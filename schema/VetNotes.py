vetnotes_scheme={
    "type": "object",
    "properties": {
         "SUMMARY": {
            "type": "string",
            "description": "Summary of the vet notes"
         },
         "CHECK":{
            "type": "string",
            "description": "Why we came in / What was Observed"
         },
         "ASSESS":{
            "type": "string",
            "description": "Vet's interpretation and explanation"
         },
         "RESPONSE":{
         "type":"string",
         "description":"Treatment and recommendations"
         },
         "EVALUATE":{
            "type":"string",
            "description":"Understanding and Next Steps"
         }   
    },
    "required": ["SUMMARY","CHECK","ASSESS","RESPONSE","EVALUATE"],
    "additionalProperties": False
}