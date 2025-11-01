from constants.FetchConstants import fetch_constants

def calculate_diagnosis(metric:str,value: float) -> str:
    try:
        low_range=fetch_constants.get(metric)["USC"].get("LOW")
        normal_range=fetch_constants.get(metric)["USC"].get("NORMAL")
        mild_range=fetch_constants.get(metric)["USC"].get("MILD")
        elevated_range=fetch_constants.get(metric)["USC"].get("ELEVATED")
        severe_range=fetch_constants.get(metric)["USC"].get("SEVERE")
                
        if low_range and value>=low_range["LOWER_BOUND"] and value <=low_range["UPPER_BOUND"]:
            return "LOW"
        if normal_range and value>=normal_range["LOWER_BOUND"] and value <=normal_range["UPPER_BOUND"]:
            return "NORMAL"
        if mild_range and value>=mild_range["LOWER_BOUND"] and value <=mild_range["UPPER_BOUND"]:
            return "MILD"
        if elevated_range and value>=elevated_range["LOWER_BOUND"] and value <=elevated_range["UPPER_BOUND"]:
            return "ELEVATED"
        if severe_range and value>=severe_range["LOWER_BOUND"]:
            return "SEVERE"
        return "OUT OF RANGE"
    except (ValueError, TypeError):
        return None

def calculate_iris_stage(sdma_value, creatinine_value) -> dict:
    """
    Calculate IRIS (International Renal Interest Society) CKD stage based on SDMA and creatinine values
    
    IRIS CKD Staging Guidelines:
    - Stage 1 (At risk): SDMA <18, Creatinine <1.6 mg/dL
    - Stage 2 (Mild): SDMA 18-25, Creatinine 1.6-2.8 mg/dL  
    - Stage 3 (Moderate to severe): SDMA 26-38, Creatinine 2.9-5.0 mg/dL
    - Stage 4 (Most severe): SDMA >38, Creatinine >5.0 mg/dL
    """
    try:
        # Handle None or empty values
        if sdma_value is None or sdma_value == "" or creatinine_value is None or creatinine_value == "":
            return {
                "VALUE": None,
                "LOWER_BOUND": "1",
                "UPPER_BOUND": "4", 
                "UNITS": "stage",
                "DIAGNOSIS": None
            }
        
        sdma = float(sdma_value)
        creatinine = float(creatinine_value)
        
        # Determine stage based on IRIS guidelines
        # IRIS staging is primarily based on creatinine, with SDMA as supporting evidence
        
        if creatinine > 5.0:
            stage = 4
        elif creatinine >= 2.9:
            stage = 3
        elif creatinine >= 1.6:
            stage = 2
        else:
            stage = 1
            
        # If creatinine suggests stage 1 but SDMA is elevated, consider SDMA
        if stage == 1 and sdma >= 18:
            if sdma >= 38:
                stage = 4
            elif sdma >= 26:
                stage = 3
            else:  # sdma 18-25
                stage = 2

        return {
            "VALUE": stage,
            "LOWER_BOUND": "1",
            "UPPER_BOUND": "4",
            "UNITS": "stage", 
            "DIAGNOSIS": stage
        }
        
    except (ValueError, TypeError):
        return {
            "VALUE": None,
            "LOWER_BOUND": "1", 
            "UPPER_BOUND": "4",
            "UNITS": "stage",
            "DIAGNOSIS": None
        }
