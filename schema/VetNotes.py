from sqlalchemy.orm import context


context_text='''
   Tone: Warm, supportive, feminine, and knowledgeable.


   Voice: Calm and confident — a blend of vet nurse + kind friend.


   Goal: Help owners feel informed, capable, and comforted after the visit.


   Language: Use short sentences. Avoid jargon. Define terms gently (e.g., “Creatinine — a measure of kidney filtration.”).


   Perspective: Neutral and factual but emotionally aware — e.g., “The vet reassured that this is manageable,” instead of “The vet said it’s not serious.”

   If some information is missing, infer gently (“The vet did not mention next steps, but typical CKD monitoring includes…”).


   Use the same warm, confident tone as Hugging Cat’s other outputs — medical clarity with empathy and calm reassurance.


   Include short paragraphs or bullet points for readability.

   Emojis like 💛 💧 💊 📅 🌿 can be used sparingly to convey friendliness.

   IMPORTANT: BASE YOUR RESPONSE ON THE PROVIDED DATA ONLY. IF THERE IS NO RELEVANT DATA, JUST SAY THERE IS NO DATA FOR THIS SECTION IN THE AUDIO.
'''
vetnotes_scheme={
    "type": "object",
    "properties": {
         "SUMMARY": {
            "type": "string",
            "description": context_text + "Provide a brief, compassionate overview of the entire vet visit. Capture the main concern, diagnosis, and care plan in 2-3 sentences that help the owner remember the visit's key takeaway."
         },
         "CHECK":{
            "type": "string",
            "description": context_text + "Summarize why the visit happened and what the owner/vet observed. Include symptoms, concerns, or physical changes in a kind, simple way."+' Example: “Owner brought Luna in for increased thirst, occasional vomiting, and decreased appetite. Vet noted mild dehydration and weight loss.”'
         },
         "ASSESS":{
            "type": "string",
            "description": context_text + "Summarize the vet’s interpretation, findings, and reasoning. Include any lab results, explanations, or diagnoses discussed. Explain medical terms gently."+' Example: “The vet explained that Luna’s kidney values are rising slightly, indicating early CKD progression. They reassured this is manageable with close care and hydration.”'
         },
         "RESPONSE":{
         "type":"string",
         "description": context_text + "List what the vet recommended or prescribed. Include diet, meds, fluids, supplements, and follow-ups. Use friendly bullet points with brief reasoning."+' Example:💊 Continue renal diet and encourage wet food.\n💧 Give 100 mL sub-q fluids twice weekly.\n📅 Recheck labs in 6 weeks.'

         },
         "EVALUATE":{
            "type":"string",
            "description": context_text + "Summarize what happens next. Capture the owner's understanding, emotional tone, and what to watch at home."+'Example: “The owner understood the plan and will track appetite, energy, and hydration. The next visit will focus on phosphorus and blood pressure.”'

         }   
    },
    "required": ["SUMMARY","CHECK","ASSESS","RESPONSE","EVALUATE"],
    "additionalProperties": False
}