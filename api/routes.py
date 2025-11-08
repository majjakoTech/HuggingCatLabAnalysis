import json
from fastapi import APIRouter, UploadFile, File
from typing import List
from openai import OpenAI
from db.postgres import get_postgres_db
from model.CatData import CatData
from model.Users import Users
from schema.Fetch import schema
from schema.VetNotes import vetnotes_scheme
from schema.VetChecklist import vet_checklist_scheme
from utils.Medical import calculate_diagnosis, calculate_iris_stage
from utils.Common import process_file,save_images,save_vet_data,save_vet_checklist
from typing import Optional
from dummy.Transcription import text
from constants.KeyMetricConstants import metrics

router=APIRouter()
client = OpenAI()
db=next(get_postgres_db())

@router.post('/users/{user_id}/fetch-data')
async def fetchData(
    user_id: int,
    images: List[UploadFile]=File(..., description="Images or PDF files")
):

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
        
        try:
            analysis_json = json.loads(analysis_text)

            include_metrics=metrics

            for metric in include_metrics:
                data=analysis_json.get(metric)
    
                if data is not None and data.get("VALUE") is not None and isinstance(data.get("VALUE"), (int, float)):
            
                    calculated_diagnosis = calculate_diagnosis(metric,data["VALUE"])
                    analysis_json[metric]["INTERPRETATION"]=calculated_diagnosis
                

            sdma=analysis_json.get("BLOOD_SYMMETRIC_DIMETHYLARGININE_SDMA")
            creatinine=analysis_json.get("BLOOD_CREATININE")

            if sdma and creatinine:
                if "VALUE" in sdma and "VALUE" in creatinine:
                    iris_stage_data = calculate_iris_stage(sdma["VALUE"], creatinine["VALUE"])
                    analysis_json["IRIS_STAGE"] = iris_stage_data            
            
          
            paths=await save_images(images)
            
            cat_data=CatData(
            data=analysis_json,
            user_id=user_id,
            lab_reports=paths
        )
            db.add(cat_data)
            db.commit()
            

            show_medical_params=metrics

            result_data = {}
            for param in show_medical_params:
                if param in analysis_json and analysis_json[param] is not None:
                    if "INTERPRETATION" in analysis_json[param]:
                        result_data[param] = analysis_json[param]["INTERPRETATION"]
                    elif "DIAGNOSIS" in analysis_json[param]:
                        result_data[param] = analysis_json[param]["DIAGNOSIS"]
                    else:
                        result_data[param] = analysis_json[param].get("VALUE")
            
            
            return {
                "success": True,
                "analysis": result_data
            }
        except json.JSONDecodeError as json_error:
            return {
                "success": False,
                "error": f"JSON parsing failed: {str(json_error)}",
                "raw_response": cleaned_text[:500] + "..." if len(cleaned_text) > 500 else cleaned_text,
                "original_response": analysis_text[:200] + "..." if len(analysis_text) > 200 else analysis_text
            }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "images_processed": 0
        }



@router.get('/users/{user_id}/overview')
async def overview(user_id: int):
    cat_data=db.query(CatData).filter_by(user_id=user_id).first()
  
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

    return {
        "success": True,
        "overview": response.choices[0].message.content
    }

@router.get('/users/{user_id}/summary')
async def summary(user_id: int):
    cat_data=db.query(CatData).filter_by(user_id=user_id).first()
  
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

    return {
        "success": True,
        "overview": response.choices[0].message.content
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

    cat_data=db.query(CatData).filter_by(user_id=user_id).first()
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
   
    return {
        "success": True,
        "analysis": analysis_json,
        "data":selected_data
    }

@router.post('/vet-notes/users/{user_id}/analyze')
async def category(user_id: int,audio:UploadFile=File(...)):
    try:
        audio_content = await audio.read()
        transcription=client.audio.transcriptions.create(model="whisper-1",file=(audio.filename, audio_content, audio.content_type))
    
        response_scheme=vetnotes_scheme

        cat_data=db.query(CatData).filter_by(user_id=user_id).first()
        cat_name=cat_data.data["NAME"]

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
        await save_vet_data(transcription.text,analysis_json,user_id,audio)

        return {
            "success": True,
            "analysis":analysis_json
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@router.get('/vet-notes/users/{user_id}')
def get_vet_notes(user_id: int):
    user=db.query(Users).filter_by(id=user_id).first()

    return user.vet_notes
    
@router.get('/vet-checklist/users/{user_id}/analyse')
def get_vet_checklist(user_id: int):

    user=db.query(Users).filter_by(id=user_id).first()
    care_notes=user.vet_notes[0]['analysis']
    cat_data=db.query(CatData).filter_by(user_id=user_id).first().data

    response_scheme=vet_checklist_scheme

    user_prompt=f"""
    CARE NOTES:
    {care_notes}
    CAT DATA:
    {cat_data}
    """
    
    analysis=client.chat.completions.create(
            model="gpt-4o-mini",  
            messages=[

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
    
    return analysis_json


@router.get('/vet-checklist/users/{user_id}')
def get_vet_checklist(user_id: int):
    user=db.query(Users).filter_by(id=user_id).first()

    return user.vet_checklist