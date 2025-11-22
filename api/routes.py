import json
from fastapi import APIRouter, UploadFile, File
from typing import List
from openai import OpenAI
from db.postgres import get_postgres_db
from datetime import datetime
from model.CatData import CatData
from model.LabAnalysis import LabAnalysis
from model.Users import Users
from model.VetNote import VetNote
from schema.Fetch import schema
from schema.VetNotes import vetnotes_scheme
from schema.VetChecklist import vet_checklist_scheme
from utils.Medical import interpret_value, calculate_iris_stage
from utils.Common import process_file,save_images,save_vet_data,save_vet_checklist,check_user_exists
from typing import Optional
from dummy.Transcription import text
from constants.KeyMetricConstants import metrics
from utils.Medical import show_medical_params,interpret_bacteria_value,interpret_wbc_value,interpret_culture_value,diagnose_inflamation,diagnose_infection
from fastapi import HTTPException
from constants.CommonConstants import lab_analysis_categories

router=APIRouter()
client = OpenAI()


@router.post('/users/{user_id}/lab-reports')
async def fetchDataReport(
    user_id: int,
    images: List[UploadFile]=File(..., description="Images or PDF files")
):
    db=next(get_postgres_db())
    check_user_exists(user_id,db)

    response_schema = schema
    
    content_blocks=[]
    
    for file in images:
        
        processed_images = await process_file(file)
        for img_base64 in processed_images:
            content_blocks.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{img_base64}"
                }
            })
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  
            messages=[
                {
                    "role": "user",
                    "content": content_blocks
                }
            ],
            max_tokens=4000,
            temperature=0,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "image_analysis",
                    "schema": response_schema,
                    "strict": True
                }
            }
        )
        
        analysis_text = response.choices[0].message.content
        
       
        analysis_json = json.loads(analysis_text)

        include_metrics=metrics

        for metric in include_metrics:
            data=analysis_json.get(metric)
    
            if data is not None and data.get("VALUE") is not None and isinstance(data.get("VALUE"), (int, float)):
            
                interpretation = interpret_value(metric,data["VALUE"])
                analysis_json[metric]["INTERPRETATION"]=interpretation
                
        sdma=analysis_json.get("BLOOD_SYMMETRIC_DIMETHYLARGININE_SDMA")
        creatinine=analysis_json.get("BLOOD_CREATININE")
            
        urine_bacteria=analysis_json.get("URINE_BACTERIA")["VALUE"]
        urine_wbc=analysis_json.get("URINE_WHITE_BLOOD_CELL_WBC")["VALUE"]
        urine_culture=analysis_json.get("URINE_CULTURE_AND_SENSITIVITY")["VALUE"]

        urine_bacteria_interpretation=interpret_bacteria_value(urine_bacteria)
        urine_wbc_interpretation=interpret_wbc_value(urine_wbc)
        urine_culture_interpretation=interpret_culture_value(urine_culture)

        if urine_bacteria_interpretation:
            analysis_json["URINE_BACTERIA"]["INTERPRETATION"]=urine_bacteria_interpretation
        if urine_wbc_interpretation:
            analysis_json["URINE_WHITE_BLOOD_CELL_WBC"]["INTERPRETATION"]=urine_wbc_interpretation
        if urine_culture_interpretation:
            analysis_json["URINE_CULTURE_AND_SENSITIVITY"]["INTERPRETATION"]=urine_culture_interpretation
            

        if sdma and creatinine:
            if "VALUE" in sdma and "VALUE" in creatinine:
                iris_stage_data = calculate_iris_stage(sdma["VALUE"], creatinine["VALUE"])
                analysis_json["IRIS_STAGE"]={}
                analysis_json["IRIS_STAGE"]["VALUE"] = iris_stage_data            
            
        if urine_wbc_interpretation:
            analysis_json["URINE_INFLAMMATION"]={}
            analysis_json["URINE_INFLAMMATION"]["INTERPRETATION"]=diagnose_inflamation(urine_wbc_interpretation) 

        if urine_culture_interpretation or (urine_bacteria_interpretation and urine_wbc_interpretation) or (urine_bacteria_interpretation and urine_culture_interpretation):
            analysis_json["URINE_INFECTION"]={}
            analysis_json["URINE_INFECTION"]["INTERPRETATION"]=diagnose_infection(urine_wbc_interpretation,urine_bacteria_interpretation,urine_culture_interpretation) 

        paths=await save_images(images)


        cat_data=CatData(
            data=analysis_json,
            user_id=user_id,
            lab_reports=paths,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.add(cat_data)
        db.commit()
            
        result_data=show_medical_params(analysis_json)
        return {
            "success": True,
            "data": result_data
        }
    except Exception as e:
        db.rollback()
        return {
                "success": False,
                "error": str(e)
            }
    finally:
        db.close()

@router.get('/users/{user_id}/lab-reports')
async def labOverfetchDataDB(user_id: int):
    db=next(get_postgres_db())
    try:
        cat_data=db.query(CatData).filter_by(user_id=user_id).order_by(CatData.created_at.desc()).first()
        metrics_analysis=show_medical_params(cat_data.data)

        data={
            "success": True,
            "data": metrics_analysis
        }
        return data

    except AttributeError as e:
        return {
            "success": False,
            "error": f"No lab data found for user {user_id}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@router.get('/users/{user_id}/overview-lab-analysis')
async def overviewLabAnalysis(user_id: int):
    db=next(get_postgres_db())
    check_user_exists(user_id,db)

    try:
        cat_data=db.query(CatData).filter_by(user_id=user_id).order_by(CatData.created_at.desc()).first()
        created_at=cat_data.created_at
        if not cat_data:
            raise HTTPException(status_code=404, detail="No lab data found for user")
        if cat_data.overview_lab_analysis:
            return {
                "success": True,
                "overview": cat_data.overview_lab_analysis,
                "created_at":cat_data.created_at
            }
        
    
        user_prompt=f"""
            “Create a TL;DR Overview summary for my CKD cat using the data below.
                This should be a short, emotionally warm, yet medically grounded overview of the Key Findings.”

                
                {json.dumps(cat_data.data, indent=2)}
                

                Instructions for the AI
                Summarize the entire health picture in 4–6 sentences max.

                It should feel like a warm spoken summary from a CKD expert — part doctor, part best friend.


                Include these elements naturally:


                Overall kidney trend (stable / improving / declining).


                Most important positive (e.g., phosphorus control, hydration, appetite).


                Main area of concern (e.g., high BP, mild anemia, rising creatinine).


                Tone of direction (e.g., “stable with a few watch points,” “showing gentle progress,” “needs closer monitoring”).


                Encouraging next step (“With fluids and your vet’s guidance, she can stay stable.”).


                Avoid excessive detail or numeric values — this is emotional + directional, not technical.

                Example:

                “Her kidney values are holding steady, which is great news, though her blood pressure could use a little attention. Her electrolytes and appetite are good, and with hydration and continued care, she’s on a stable path.”


                Keep sentences short, fluid, and positive — avoid clinical stiffness.



                Tone & Style
                Empathetic, feminine, emotionally grounded.


                Use gentle transitions (“overall,” “meanwhile,” “on the bright side,” “with care and monitoring…”).


                Use simple but intelligent vocabulary — no jargon unless it’s familiar to CKD owners (like “creatinine,” “phosphorus”).


                Keep it realistic but hopeful.



                Output Structure
                Example Output:
                💛 Overall: Kidney values are moderately high but stable, suggesting her care plan is helping.
                💧 Positives: Hydration and phosphorus levels look good, both key for slowing CKD.
                ⚠️ Watch Points: Blood pressure is slightly up and mild anemia may be emerging.
                🌿 Next Steps: Keep fluids consistent and recheck BP soon — you’re helping her stay comfortable and steady.

                These insights are for learning and support — please confirm all care decisions with your veterinarian.

                Microcopy Cues for Tone
                Situation
                Example Line
                Stable cat
                “Her labs show a steady, well-managed CKD picture — that’s a real win.”
                Improving cat
                “Her numbers are gently improving, reflecting the love and consistency in her care.”
                Slightly worsening
                “A few values are trending higher, but nothing unmanageable with close vet guidance.”
                High BP
                “Her blood pressure needs attention soon, but early action helps protect her eyes and brain.”
                Low phosphorus
                “Her phosphorus control is excellent — that’s one of the best ways to keep her feeling good.”

                Formatting Guidelines
                Limit to 1 short paragraph or 3–5 compact bullet points.


                Use clear emoji cues (💛 💧 ⚠️ 🌿) sparingly but warmly.


                End with the gentle reminder line.


                No bold, italics, or technical table formatting — this is conversational and emotionally lightweight.



                Closing Reminder
                These insights are for learning and support — please confirm all care decisions with your veterinarian.
        
        """

        system_prompt=f"""
                        You are “Hugging Cat Companion,” the world’s most knowledgeable feline CKD care guide.
                        Your task is to write a brief, emotionally intelligent, and clinically accurate TL;DR overview that summarizes the overall health picture for a CKD cat based on her latest lab results.
                        This is the top-level “snapshot” section that appears before the detailed Key Findings.
                        It should give the reader — typically a woman cat parent — a quick sense of how her cat is doing:
                        what’s stable, what’s concerning, and what needs gentle attention next.
                        Your voice should sound calm, compassionate, and reassuring, with quiet authority.
                        Blend technical confidence with empathy. Keep it short and heart-centered.
                        Always end with:
                        “These insights are for learning and support — please confirm all care decisions with your veterinarian.”

        """
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",  
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            max_tokens=1000,
            temperature=0.4,
        
        )

        data=response.choices[0].message.content
        cat_data.overview_lab_analysis=data
        db.add(cat_data)
        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e)) 
    finally:
        db.close()

    return {
        "success": True,
        "overview_lab_analysis": data,
        "created_at":created_at
    }

@router.get('/users/{user_id}/key-findings')
async def key_findings(user_id: int):
    db=next(get_postgres_db())
    check_user_exists(user_id,db)

    try:
        cat_data=db.query(CatData).filter_by(user_id=user_id).order_by(CatData.id.desc()).first()
        created_at=cat_data.created_at
        if cat_data.key_findings:
            return {
                "success": True,
                "key_findings": cat_data.key_findings,
                "created_at":cat_data.created_at
            }
        prompt=f"""

                Create a Key Findings summary for this CKD cat using the lab results provided below.
                Focus on what matters most — the top concerns, the positives, the watch points, and next steps — in plain, confident language.
                Don't include the first heading like "Key Findings" in the response.

                Current Lab Data (JSON):

                {json.dumps(cat_data.data, indent=2)}

                Instructions for the AI

                1. Review all sections and metrics from the lab data.


                2.Identify the most important patterns:


                        What’s high risk or severe


                        What’s stable or improving


                        What’s missing or needs rechecking


                        What’s encouraging progress


                3.Write a concise summary that blends technical interpretation and emotional reassurance.
            
            Structure of the Output
            Top Concerns (Most Important First)
            3–6 bullets.


            Each bullet should look like this:

            Creatinine (Elevated, 4.2 mg/dL) — indicates toxin buildup; combined with low urine concentration, confirms kidney decline. Worth discussing hydration or sub-q fluid support with your vet.


            Include urgent/emergent notes (e.g., “EMERGENT: High blood pressure >180 mmHg can risk eye or brain damage — call your vet soon.”)


            Bright Spots (What’s Going Well)
            2–5 short bullets.


            Highlight improvements or normal results that protect kidney comfort (e.g., “Phosphorus in target range — great for slowing CKD progression.”)


            Watch List (Monitor Closely)
            3–6 bullets.


            Focus on mild abnormalities or trending values (e.g., “Potassium on the low end — watch for weakness or appetite changes.”)


            Trends & Relationships
            2–5 statements showing how results are moving or interrelated:


            “Creatinine up slightly from last check (3.7 → 4.2 mg/dL).”


            “Low USG + high SDMA = kidney filtration loss, not dehydration.”


            Data Gaps That Limit Confidence
            Note any missing high-value metrics (e.g., UPC, BP, PTH, bicarbonate).


            Explain why each would matter briefly (“A UPC helps detect protein loss, which can speed CKD progression.”)


            Kind Next Steps to Discuss With Your Vet
            Group ideas by theme — soft and supportive wording:
            Hydration: “Ask your vet about a sub-q fluid plan.”


            Phosphorus Control: “A renal diet or binder can help if phosphorus rises above 6.0.”


            Blood Pressure: “If BP stays above 170, meds like amlodipine may help.”


            Anemia: “B-vitamins, iron, or EPO support can improve energy.”


            Comfort: “Anti-nausea meds or appetite stimulants can help on low-appetite days.”


            Gentle One-Paragraph Summary
            Write one short, flowing paragraph that connects the big picture:
            “Your cat’s kidneys are under stress, but her phosphorus and electrolytes look good — these are protective signs. With hydration and regular monitoring, she can stay stable and comfortable. Keep working closely with your vet — you’re doing a wonderful job caring for her.”

            Tone & Style
            Gentle, warm, intelligent, and feminine.


            Sound like a smart friend who deeply understands CKD, not a robotic report.


            Keep sentences short and scannable.


            Use bold for metrics and bullets for clarity.


            Never sound alarmist; always pair concern with calm action.



            Closing Reminder
            “These explanations are for learning and support — please confirm medical decisions with your veterinarian.”

                        
        """
        response = client.chat.completions.create(
            model="gpt-4o-mini",  
            messages=[
                {
                    "role": "system",
                    "content": '''You are “Hugging Cat Companion,” the world’s most knowledgeable feline CKD care guide.
                                    Your role is to create a clear, compassionate, and clinically confident summary of a cat’s lab report — specifically, the Key Findings section.
                                    This section gives the pet parent a unified overview of the report: what’s most concerning, what’s stable or improving, what to monitor, and what to discuss next with their vet.
                                    Write in a warm, intelligent, and reassuring tone — as if explaining the findings to a thoughtful woman cat owner who wants to understand and support her cat deeply.
                                    Use medical precision but everyday clarity. Blend science and empathy.
                                    Always close with:
                                    “These explanations are for learning and support — please confirm medical decisions with your veterinarian.”
                                '''
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=1400,
            temperature=0.4,
        
        )
        data=response.choices[0].message.content
       
    
        if data:
            cat_data.key_findings=data
            db.commit()


    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        db.close()
    
    return {
        "success": True,
        "key_findings":data,
        "created_at":created_at
    }


categories={
    "RA":{
        "title":"Renal Health",
        "metrics":["BLOOD_SYMMETRIC_DIMETHYLARGININE_SDMA",
        "BLOOD_UREA_NITROGEN_BUN","BLOOD_CREATININE",
        "BLOOD_BUN_CREATININE_RATIO","BLOOD_PHOSPHORUS_PHOSPHATE"]
    },
    "EA":{
        "title":"Electrolytes",
        "metrics":["BLOOD_SODIUM",
        "BLOOD_POTASSIUM",
        "BLOOD_CHLORIDE","BLOOD_CALCIUM",
        "BLOOD_PHOSPHORUS_PHOSPHATE",
        "BLOOD_MAGNESIUM","BLOOD_SODIUM_POTASSIUM_RATIO_NAK"]
    },
    "BPA":{
        "title":"Blood Pressure",
        "metrics":["SYSTOLIC_BLOOD_PRESSURE","DIASTOLIC_BLOOD_PRESSURE"]
    },
    "RBCA":{
        "title":"Red Blood Cell Analysis",
        "metrics":["BLOOD_RED_BLOOD_CELL_RBC",
        "BLOOD_HEMOGLOBIN_HGB",
        "BLOOD_HEMATOCRIT_HCT",
        "BLOOD_MEAN_CORPUSCULAR_VOLUME_MCV",
        "BLOOD_MEAN_CORPUSCULAR_HEMOGLOBIN_CONCENTRATION_MCHC",
        "BLOOD_RED_CELL_DISTRIBUTION_WIDTH_RDW",
        "BLOOD_TOTAL_PROTEIN"
        ,"BLOOD_ALBUMIN",
        "BLOOD_GLOBULIN","BLOOD_PLATELET_COUNT"]
    },
    "WBCA":{
        "title":"White Blood Cell Analysis",
        "metrics":["BLOOD_WHITE_BLOOD_CELL_WBC","BLOOD_NEUTROPHILS","BLOOD_LYMPHOCYTES","BLOOD_MONOCYTES","BLOOD_EOSINOPHILS","BLOOD_BASOPHILS"]
    },
    "LEA":{
        "title":"Liver Enzyme Analysis",
        "metrics":["BLOOD_ALANINE_AMINOTRANSFERASE_ALT_SERUM_GLUTAMATE_PYRUVATE_TRANSFERASE_SGPT",
        "BLOOD_ASPARTATE_AMINOTRANSFERASE_AST_SERUM_GLUTAMATE_OXALOACETATE_TRANSFERASE_SGOT",
        "BLOOD_ALKALINE_PHOSPHATASE_ALP",
        "BLOOD_GAMMA_GLUTAMYL_TRANSFERASE_GGT",
        "BLOOD_BILIRUBIN","BLOOD_ALBUMIN","BLOOD_GLOBULIN"]
    },
    "PEA":{
        "title":"Pancreatic Enzyme Analysis",
        "metrics":["BLOOD_AMYLASE","BLOOD_PRECISION_PSL",
        "BLOOD_CREATINE_PHOSPHOKINASE"]
    },
    "TFA":{
        "title":"Thyroid Function Analysis",
        "metrics":["BLOOD_TOTAL_THYROXINE_T4"]
    },

    "UA":{
        "title":"Urinalysis",
        "metrics":[
        "URINE_COLOR",
        "URINE_SPECIFIC_GRAVITY",
        "URINE_PH",
        "URINE_PROTEIN",
        "URINE_GLUCOSE_STRIP",
        "URINE_BILIRUBIN",
        "URINE_KETONES",
        "URINE_OCCULT_BLOOD",
        "URINE_WBC","URINE_RBC",
        "URINE_CASTS","URINE_CRYSTALS"
        ,"URINE_BACTERIA",
        "URINE_EPITHELIAL_CELL",
        "URINE_FAT_DROPLETS"]
    }

}
@router.get('/users/{user_id}/analysis')
async def analyseData(user_id: int ,category: str):
    try:
        db=next(get_postgres_db())

        check_user_exists(user_id,db)
        
        if not category in lab_analysis_categories:
            raise HTTPException(status_code=400,detail="Invalid category")
        
        cat_data=db.query(CatData).filter_by(user_id=user_id).order_by(CatData.created_at.desc()).first()
        created_at=cat_data.created_at

        if not cat_data:
            raise HTTPException(status_code=404,detail="Cat data not found")

        lab_analysis=db.query(LabAnalysis).filter_by(cat_data_id=cat_data.id,name=category).first()

        if lab_analysis:
            return {
                "success": True,
                "data":lab_analysis.data,
                "created_at":created_at
            }

        data=cat_data.data

        metrics=categories[category]['metrics']

        selected_data={metric:data[metric] for metric in metrics if metric in data}

        # System prompt: Persona and behavioral guidelines
        system_prompt = '''
            You are "Hugging Cat Companion," the world's most knowledgeable feline CKD care guide.
            
            Your voice is:
            - Calm, compassionate, intelligent, and empowering
            - Warm and feminine with emotional resonance
            - Professional yet kind — "medical grade info meets best-friend support"
            
            Writing style:
            - Blend medical precision with warmth
            - Use short, reader-friendly paragraphs
            - Explain WHY values matter, not just what they are
            - Use positive framing and emphasize manageability
            - Include actionable insights naturally
            - Show relationships between metrics clearly
            
            Always end with: "These explanations are for learning and support — please confirm medical decisions with your veterinarian."
        '''
        
        # User prompt: Simple task with data
        user_prompt = f'''
            Analyze these {category} lab results for a CKD cat and provide detailed explanations for each metric:
            
            {json.dumps(selected_data, indent=2)}
        '''

        response_scheme={
            "type": "object",
            "properties": {
                    "SUMMARY": {
                            "type": "string",
                            "description": f"Create a short summary of the {category} lab results. Explain what the overall pattern means for this CKD cat's health, highlighting both concerns and positive findings. Use warm, intelligent tone as 'Hugging Cat Companion' - like speaking to a caring cat parent who wants to understand deeply. Example: 'Your cat is in IRIS Stage 3 CKD. The good news is her phosphorus is controlled, electrolytes are stable, and she doesn't currently show anemia or infection. There is toxin buildup, which explains some off days, but overall her labs show CKD that's being managed fairly well. With continued monitoring and proactive care, she can still enjoy a good quality of life.'"
                        },
                        **{metric:{
                                "type":"string",
                                "description": f"Explain {metric} for this CKD cat. Include: 1) What it measures in simple and medical terms, 2) Normal range vs current value, 3) What high/low means for CKD cats, 4) Relationships to other markers, 5) Possible causes of abnormality, 6) Care advice (diet, hydration, supplements, meds to discuss with vet), 7) Monitoring guidance. Use warm, empathetic tone."

                            } for metric in selected_data}
            },
            "required": ["SUMMARY",*selected_data],
            "additionalProperties": False
        }
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",  
            messages=[
                {
                    "role":"system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            max_tokens=1400,
            temperature=0.4,
        response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "analysis",
                        "schema": response_scheme,
                        "strict": True
                    }
                }
        )
            
        analysis_text = response.choices[0].message.content

        
        analysis_json = json.loads(analysis_text)

        try:
            lab_analysis=LabAnalysis(
                name=category,
                data={**analysis_json, 
                    "data":selected_data,
                },
                cat_data_id=cat_data.id,
                created_at=created_at,
            )
            db.add(lab_analysis)
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500,detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        db.close()

    return {
        "success": True,
        "data": {**analysis_json,
            "metrics":selected_data,
        },
        "created_at":created_at
    }

@router.post('/users/{user_id}/vet-notes')
async def vetNotesAnalyze(user_id: int,audio:UploadFile=File(...)):
    db=next(get_postgres_db())
    check_user_exists(user_id,db)
    try:
       
        audio_content = await audio.read()
        transcription=client.audio.transcriptions.create(model="whisper-1",file=(audio.filename, audio_content, audio.content_type))
    
        response_scheme=vetnotes_scheme

        cat_data=db.query(CatData).filter_by(user_id=user_id).order_by(CatData.created_at.desc()).first()
        cat_name=cat_data.data["NAME"] if cat_data and cat_data.data["NAME"] else ""

        embeed_name=f"CAT NAME:{cat_name}\n"

        analysis=client.chat.completions.create(
            model="gpt-4o-mini",  
            messages=[

                {
                    "role": "user",
                    "content":embeed_name+text
                }
            ],
            max_tokens=1400,
            temperature=0.4,
        response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "analysis",
                        "schema":response_scheme,
                        "strict": True
                    }
                }
        )
        analysis_json=json.loads(analysis.choices[0].message.content)
 
        await save_vet_data(transcription.text,analysis_json,user_id,audio,db)

        notes=db.query(VetNote).filter_by(user_id=user_id).order_by(VetNote.created_at.desc()).all()
        db.close()
        return {
            "success": True,
            "data":notes
        }
    except Exception as e:
        db.rollback()
        return {
            "success": False,
            "error": str(e)
        }
    finally:
        db.close()

@router.get('/users/{user_id}/vet-notes')
def get_vet_notes(user_id: int):
    db=next(get_postgres_db())
    check_user_exists(user_id,db)
    notes=db.query(VetNote).filter_by(user_id=user_id).order_by(VetNote.created_at.desc()).all()
    db.close()
    return {
        "success": True,
        "data":notes
    }

@router.delete('/vet-notes/{note_id}')
def delete_vet_notes(note_id: int):
    db=next(get_postgres_db())
    try:
        note=db.query(VetNote).filter_by(id=note_id).first()
        db.delete(note)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        db.close()
    return {
        "success": True,
        "message": "Vet note deleted successfully"
    }


    db=next(get_postgres_db())
    user=db.query(Users).filter_by(id=user_id).first()

    return user.vet_notes
    
@router.get('/users/{user_id}/vet-checklist/analyze')
def get_vet_checklist(user_id: int):


    db=next(get_postgres_db())
    check_user_exists(user_id,db)
    
    try:
        vet_note=db.query(VetNote).filter_by(user_id=user_id).order_by(VetNote.created_at.desc()).first()
        care_notes=vet_note.analysis if vet_note else None
        
        cat_data=db.query(CatData).filter_by(user_id=user_id).order_by(CatData.created_at.desc()).first()
        if cat_data:
            cat_data=cat_data.data
        else:
            cat_data=None


        response_scheme=vet_checklist_scheme

        system_prompt = """
            You are "Hugging Cat Companion," the world's most knowledgeable and empathetic CKD care guide.

            Your task is to analyze a cat's data and care notes to create a clear, focused Next Vet Visit Checklist.
            The checklist helps the cat's owner prepare for their next appointment — highlighting the most important questions and discussion points based on recent findings, changes in care, and ongoing CKD management.

            ## Analysis Guidelines:

            Review the provided data and look for:
            - Abnormal or borderline lab values (e.g., high creatinine, phosphorus, SDMA, or low potassium, HCT, or calcium)
            - Any symptoms or changes mentioned (appetite, thirst, urination, vomiting, energy, behavior)
            - Medications or supplements currently in use (dose, timing, or tolerance review needed)
            - Diet changes or hydration strategies that may need follow-up
            - New additions or persistent problems that deserve review
            - Routine CKD checks that may be due (blood pressure, urinalysis, culture, retest timelines)

            ## Tone and Voice:
            - Calm, supportive, smart, feminine
            - Avoid alarm or clinical stiffness
            - Use words like "ask," "mention," "check," "review" instead of "must" or "should"
            - Example: "Ask if her potassium level needs a small supplement adjustment — sometimes low-normal can cause weakness."

            ## Output Requirements:
            - Keep each section short and prioritized (2-3 key items per category)
            - Only include what's timely, relevant, or needs vet review
            - Base your response ONLY on the provided data
            - If there's no relevant data for a section, write "No specific concerns based on current data" or suggest routine monitoring
            - Prioritize items: mark urgent concerns clearly
            """

        user_prompt = f"""
                Analyze the following data and create a vet visit checklist.

                ## CARE NOTES FROM LAST VISIT:
                {care_notes}

                ## LAB RESULTS & CAT DATA:
                {cat_data}
                """
        
        analysis=client.chat.completions.create(
                model="gpt-4o-mini",  
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content":user_prompt
                    }
                ],
                max_tokens=1400,
                temperature=0.4,
            response_format={
                        "type": "json_schema",
                        "json_schema": {
                            "name": "analysis",
                            "schema":response_scheme,
                            "strict": True
                        }
                    }
            )
        
        analysis_json=json.loads(analysis.choices[0].message.content)
    
        save_vet_checklist(analysis_json,user_id)
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        db.close()
    return {
        "success": True,
        "data":analysis_json
    }


@router.get('/users/{user_id}/vet-checklist')
def get_vet_checklist(user_id: int):
    db=next(get_postgres_db())
    check_user_exists(user_id,db)
    try:
        user=db.query(Users).filter_by(id=user_id).first()
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        db.close()
        
    response={
        "success": True,
        "data":user.vet_checklist,
        "created_at":user.created_at
    }
    return response