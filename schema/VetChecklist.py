vet_checklist_scheme = {
    "type": "object",
    "properties": {
        "KIDNEY_FUNCTION": {
            "type": "string",
            "description": "Questions about kidney function metrics (creatinine, SDMA, BUN, phosphorus). Include specific values if abnormal and what to ask about them."
        },
        "FLUIDS_HYDRATION": {
            "type": "string",
            "description": "Questions about fluid therapy, hydration status, and sub-q fluids. Include frequency concerns or effectiveness questions."
        },
        "DIET_SUPPLEMENT": {
            "type": "string",
            "description": "Questions about renal diet, food tolerance, and supplements (phosphorus binders, vitamins, etc.). Include dosage or timing questions."
        },
        "MEDICATIONS": {
            "type": "string",
            "description": "Questions about current medications (nausea, blood pressure, etc.). Include concerns about effectiveness, side effects, or dose adjustments."
        },
        "URINE_INFECTION": {
            "type": "string",
            "description": "Questions about urinary health, need for urinalysis or culture, changes in urination patterns."
        },
        "SYMPTOMS_BEHAVIOR": {
            "type": "string",
            "description": "Questions about observed symptoms (appetite changes, vomiting, lethargy, weight loss) and behavioral changes."
        },
        "FOLLOWUP": {
            "type": "string",
            "description": "Questions about next lab timeline, monitoring frequency, warning signs to watch for, and when to return."
        }
    },
    "required": ["KIDNEY_FUNCTION","FLUIDS_HYDRATION","DIET_SUPPLEMENT","MEDICATIONS","URINE_INFECTION","SYMPTOMS_BEHAVIOR","FOLLOWUP"],
    "additionalProperties": False
}
