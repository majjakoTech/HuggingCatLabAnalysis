from constants.FetchConstants import fetch_constants
from constants.KeyMetricConstants import metrics
from typing import Optional
import re

def interpret_value(metric:str,value: float) -> str:
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

        return stage
        
    except (ValueError, TypeError):
        return None

def show_medical_params(data:dict):
    try:
        show_medical_params=metrics

        result_data = {}
        for param in show_medical_params:
            if param in data and data[param] is not None:
                if "INTERPRETATION" in data[param]:
                    result_data[param] = data[param]["INTERPRETATION"]
                else:
                        result_data[param] = data[param].get("VALUE")
        
        return result_data
    except Exception as e:
        return str(e)

def interpret_wbc_value(raw: Optional[str]) -> Optional[str]:
    """
    Interpret urine WBC into 'POSITIVE' / 'NEGATIVE' / None.
    Only two rules:
    - Numeric threshold: max >= 5 → POSITIVE
    - Text-based clear positive/negative
    No borderline logic.
    """
    if raw is None:
        return None

    v = raw.strip().lower()
    if not v:
        return None

    # Remove "/hpf" or " hpf"
    v = re.sub(r'\s*\/?\s*hpf\b', '', v).strip()

    # CLEAR NEGATIVE words
    negative_set = {
        'none',
        'none seen',
        'not seen',
        'negative',
        'neg',
        '-',
        'no',
    }

    # CLEAR POSITIVE words
    positive_set = {
        'positive',
        'seen',
        'pos',
        'many',
        'tntc',
        'too numerous to count',
        'packed field',
        '+',
        '++',
        '+++',
    }

    # Direct text matches
    if v in negative_set:
        return "NEGATIVE"
    if v in positive_set:
        return "POSITIVE"

    # Plus symbols (e.g. "++++")
    if re.fullmatch(r'\++', v):
        return "POSITIVE"

    if v == '-':
        return "NEGATIVE"

    # Comparator: >5, >=5, <5, <=3
    m = re.match(r'^(>=|<=|>|<)\s*(\d+(\.\d+)?)$', v)
    if m:
        op, num = m.group(1), float(m.group(2))
        if op in ('>', '>='):
            return "POSITIVE" if num >= 5 else "NEGATIVE"
        if op in ('<', '<='):
            return "NEGATIVE" if num < 5 else "POSITIVE"

    # Numeric range: "0-2", "5-10"
    m = re.match(r'^(\d+(\.\d+)?)\s*[-–]\s*(\d+(\.\d+)?)$', v)
    if m:
        high = float(m.group(3))
        return "POSITIVE" if high >= 5 else "NEGATIVE"

    # Pure numeric
    if re.fullmatch(r'\d+(\.\d+)?', v):
        num = float(v)
        return "POSITIVE" if num >= 5 else "NEGATIVE"
    

    # Anything else is unknown
    return None

def interpret_bacteria_value(raw:Optional[str])->Optional[str]:
    if raw is None:
        return None

    v=raw.strip().lower()

    if not v and v!='0':
        return None 

    negative_set=[
        'none',
        'none seen',
        'not seen',
        'no',
        'no growth',
        'negative',
        'neg',
        '-',
        'nil',
        'no organism seen',
        'no organisms'
    ]

    postive_set=[
        'positive',
        'pos',
        'few',
        'few seen',
        'few organisms',
        'few rods',
        'few cocci',
        'moderate',
        'moderate numbers',
        'mod',
        'many',
        'tntc',
        'too numerous to count',
        'packed field',
        '+',
        '++',
        '+++',
        '++++',
        'rods',
        'rods seen',
        'cocci',
        'cocci seen',
        'bacilli',
    ]

    if v in negative_set:
        return "NEGATIVE"
    if v in postive_set:
        return "POSITIVE"

    return None
    

def interpret_culture_value(raw:Optional[str])->Optional[str]:
    if raw is None:
        return None

    v=raw.strip().lower()
   
    if not v and v!='0':
        return None
        
        print(v)
     
    v=re.sub(r'[cC][fF][uU]\s*\\\s*[mM][lL]', '',v)

    negative_set = [
        'no growth',
        'no bacterial growth',
        'no significant growth',
        'negative',
        'sterile',
        'sterile urine',
        'no aerobic growth',
        'no anaerobic growth',
    ]

    positive_set = [
        'growth',
        'significant growth',
        'heavy growth',
        'light growth',
        'moderate growth',
        'mixed growth',
        'bacterial growth',
        'bacterial growth present',
        'positive',
        'organism isolated',
        'isolate',
        'isolated',
        'sensitive',
        'resistant',
        "e. coli",
        "escherichia coli",
        "staph",
        "staphylococcus",
        "streptococcus",
        "enterococcus",
        "proteus",
        "klebsiella",
        "pseudomonas",
        "citrobacter",
        "enterobacter",
        "serratia",
        "bacillus",
        "corynebacterium",
        "yeast"
    ]

    if v in negative_set:
        return "NEGATIVE"
    if v in positive_set:
        return "POSITIVE"

    v=re.match(r'(\d*)(\.(\d*))?',v)

    if v:
        if float(v.group(1))>=1000:
            return "POSITIVE"
        else:
            return "NEGATIVE"
    

    return None

    
def diagnose_infection(wbc_interpretation_value,bacteria_value_interpretation_value,culture_value_interpretation_value):
    
    if culture_value_interpretation_value=="POSITIVE":
        return "POSITIVE"
    if bacteria_value_interpretation_value=="POSITIVE" and wbc_interpretation_value=="POSITIVE":
        return "POSITIVE"
    if bacteria_value_interpretation_value=="POSITIVE" and culture_value_interpretation_value=="POSITIVE":
        return "POSITIVE"
    return "NEGATIVE"

def diagnose_inflamation(wbc_value_interpretation):
    if not wbc_value_interpretation:
        return None
    if wbc_value_interpretation=="POSITIVE":
        return "POSITIVE"
    return "NEGATIVE"