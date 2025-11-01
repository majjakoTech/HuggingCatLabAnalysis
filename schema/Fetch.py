schema={
        "type": "object",
        "properties": {
                 "NAME": {
                        "type": ["string","null"]
                      
                    },
                    "AGE": {
                        "type":["number", "null"],
                       
                    },
                    "GENDER": { 
                        "type": ["string","null"]
                       
                    },
                    "BREED": {
                        "type": ["string","null"]
                       
                    },
                    "WEIGHT": {
                        "type": ["string","null"],
                       
                    },
              "BLOOD_TOTAL_PROTEIN": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type":["number", "null"],
                       
                    }
                },
                "required": ["VALUE"],
                "additionalProperties": False
            },       
            "BLOOD_UREA_NITROGEN_BUN": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type":["number", "null"],
                       
                    }
                },
                "required": ["VALUE"],
                "additionalProperties": False
            },
              "BLOOD_PHOSPHORUS_PHOSPHATE": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type":["number", "null"],
                       
                    }
                },
                "required": ["VALUE"],
                "additionalProperties": False
            }
            ,
              "URINE_PROTEIN_CREATININE_RATIO_UPC": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type":["number", "null"],
                       
                    }
                },
                "required": ["VALUE"],
                "additionalProperties": False
            }
            ,
              "BLOOD_CALCIUM": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type":["number", "null"],
                       
                    }
                },
                "required": ["VALUE"],
                "additionalProperties": False
            },
            "BLOOD_ANAEMIA": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type":["string", "null"],
                       
                    }
                },
                "required": ["VALUE"],
                "additionalProperties": False
            },
             "BLOOD_RED_BLOOD_CELL_RBC": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type":["number", "null"],
                       
                    }
                },
                "required": ["VALUE"],
                "additionalProperties": False
            },
             "BLOOD_WHITE_BLOOD_CELL_WBC": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type":["number", "null"],
                       
                    }
                },
                "required": ["VALUE"],
                "additionalProperties": False
            },
            "BLOOD_ALBUMIN": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type":["number", "null"],
                       
                    }
                },
                "required": ["VALUE"],
                "additionalProperties": False
            },
            "BLOOD_GLOBULIN": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type":["number", "null"],
                       
                    }
                },
                "required": ["VALUE"],
                "additionalProperties": False
            },
              "BLOOD_ALBUMIN_GLOBULIN_RATIO_AG": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type":["number", "null"],
                       
                    }
                },
                "required": ["VALUE"],
                "additionalProperties": False
            },
            "BLOOD_HEMATOCRIT_HCT": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type":["number", "null"],
                       
                    }
                },
                "required": ["VALUE"],
                "additionalProperties": False
            },
        
            "BLOOD_ALANINE_AMINOTRANSFERASE_ALT_SERUM_GLUTAMATE_PYRUVATE_TRANSFERASE_SGPT": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type":["number", "null"],
                       
                    }
                },
                "required": ["VALUE"],
                "additionalProperties": False
            },
            "BLOOD_MEAN_CORPUSCULAR_VOLUME_MCV": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type":["number", "null"],
                       
                    }
                },
                "required": ["VALUE"],
                "additionalProperties": False
            },
            "BLOOD_BUN_CREATININE_RATIO": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type":["number", "null"],
                    }
                },
                "required": ["VALUE"],
                "additionalProperties": False
            },
            "BLOOD_ASPARTATE_AMINOTRANSFERASE_AST_SERUM_GLUTAMATE_OXALOACETATE_TRANSFERASE_SGOT": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type":["number", "null"],
                    }
                },
                "required": ["VALUE"],
                "additionalProperties": False
            },
            "BLOOD_ALKALINE_PHOSPHATE_ALP": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type":["number", "null"],
                    }
                },
                "required": ["VALUE"],
                "additionalProperties": False
            },
            "BLOOD_GLUCOSE": {    
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type":["number", "null"],
                    }
                },
                "required": ["VALUE"],
                "additionalProperties": False
            },
            "BLOOD_CREATININE": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type":["number", "null"],
                    }
                },
                "required": ["VALUE"],
                "additionalProperties": False
            },
            "BLOOD_SYMMETRIC_DIMETHYLARGININE_SDMA": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type":["number", "null"],
                    }
                },
                "required": ["VALUE"],
                "additionalProperties": False
            },
            "BLOOD_SODIUM": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type":["number", "null"],
                    }
                },
                "required": ["VALUE"],
                "additionalProperties": False
            },
            "BLOOD_POTASSIUM": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type":["number", "null"],
                    }
                },
                "required": ["VALUE"],
                "additionalProperties": False
            },
              "BLOOD_SODIUM_POTASSIUM_RATIO_NAK": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type":["number", "null"],
                    }
                },
                "required": ["VALUE"],
                "additionalProperties": False
            },
              "BLOOD_CHLORIDE": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type":["number", "null"],
                    }
                },
                "required": ["VALUE"],
                "additionalProperties": False
            }
            ,
            "BLOOD_MEAN_CORPUSCULAR_HEMOGLOBIN_MCH": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type":["number", "null"],
                    }
                },
                "required": ["VALUE"],
                "additionalProperties": False
            },
              "BLOOD_MEAN_CORPUSCULAR_HEMOGLOBIN_CONCENTRATION_MCHC": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type":["number", "null"],
                    }
                },
                "required": ["VALUE"],
                "additionalProperties": False
            },
            "BLOOD_PLATELET_COUNT": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type":["number", "null"],
                    }
                },
                "required": ["VALUE"],
                "additionalProperties": False
            },
            "BLOOD_NEUTROPHILS": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type":["number", "null"],
                    }
                },
                "required": ["VALUE"],
                "additionalProperties": False
            },
            "BLOOD_LYMPHOCYTES": {    
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type":["number", "null"],
                    }
                },
                "required": ["VALUE"],
                "additionalProperties": False
            },
            "BLOOD_MONOCYTES": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type":["number", "null"],
                    }
                },
                "required": ["VALUE"],
                "additionalProperties": False
            },
            "BLOOD_EOSINOPHILS": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type":["number", "null"],
                    }
                },
                "required": ["VALUE"],
                "additionalProperties": False
            },
            "BLOOD_BASOPHILS": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type":["number", "null"],
                    }
                },
                "required": ["VALUE"],
                "additionalProperties": False
            },
            "BLOOD_BANDS": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type": ["number", "null"],
                    }
                },
                "required": ["VALUE"],
                "additionalProperties": False
            },
            "URINE_COLLECTION_METHOD": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type": ["string","null"]
                    }
                },
                "required": ["VALUE"],
                "additionalProperties": False
            },
            "URINE_COLOR": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type": ["string","null"]
                    }
                },
                "required": ["VALUE"],
                "additionalProperties": False
            },
            "URINE_APPEARANCE": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type": ["string","null"]
                    }
                },
                "required": ["VALUE"],
                "additionalProperties": False
            },
            "URINE_SPECIFIC_GRAVITY": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type": ["number", "null"],
                    }
                },
                "required": ["VALUE"],
                "additionalProperties": False
            },
            "URINE_PH": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type":["number", "null"],
                    }
                },
                "required": ["VALUE"],
                "additionalProperties": False
            },
            "URINE_PROTEIN": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type": ["string","null"]
                    },
                    "DIAGNOSIS": {
                        "type": ["string","null"],
                        "enum": ["NEGATIVE", "POSITIVE"],
                    },
                },
                "required": ["VALUE", "DIAGNOSIS"],
                "additionalProperties": False
            },
            "URINE_GLUCOSE_STRIP": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type": ["string","null"]
                    },
                    "DIAGNOSIS": {
                        "type": ["string","null"],
                        "enum": ["NEGATIVE", "POSITIVE"],
                    }
                },
                "required": ["VALUE", "DIAGNOSIS"],
                "additionalProperties": False
            },
            "URINE_BILIRUBIN": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type": ["string","null"]
                    },
                    "DIAGNOSIS": {
                        "type": ["string","null"],
                        "enum": ["NEGATIVE", "POSITIVE"],
                    }
                },
                "required": ["VALUE", "DIAGNOSIS"],
                "additionalProperties": False
            },
            "URINE_KETONES": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type": ["string","null"]
                    },
                    "DIAGNOSIS": {
                        "type": ["string","null"],
                        "enum": ["NEGATIVE", "POSITIVE"],
                    }
                },
                "required": ["VALUE", "DIAGNOSIS"],
                "additionalProperties": False
            },
            "URINE_OCCULT_BLOOD": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type": ["string","null"]
                    },
                    "DIAGNOSIS": {
                        "type": ["string","null"],
                        "enum": ["NEGATIVE", "POSITIVE"],
                    }
                },
                "required": ["VALUE", "DIAGNOSIS"],
                "additionalProperties": False
            },
            "URINE_WHITE_BLOOD_CELL_WBC": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type": ["string","null"]
                    },
                    "DIAGNOSIS": {
                        "type": ["string","null"],
                        "enum": ["SEEN", "NOT_SEEN"],
                    }
                },
                "required": ["VALUE", "DIAGNOSIS"],
                "additionalProperties": False
            },
            "URINE_RED_BLOOD_CELL_RBC": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type": ["string","null"]
                    },
                    "DIAGNOSIS": {
                        "type": ["string","null"],  
                        "enum": ["SEEN", "NOT_SEEN"],
                    }
                },
                "required": ["VALUE", "DIAGNOSIS"],
                "additionalProperties": False
            },
            "URINE_CASTS": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type": ["string","null"]
                    },
                    "DIAGNOSIS": {
                        "type": ["string","null"],
                        "enum": ["SEEN", "NOT_SEEN"],
                    }
                },
                "required": ["VALUE", "DIAGNOSIS"],
                "additionalProperties": False
            },
            "URINE_CRYSTALS": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type": ["string","null"]
                    },
                    "DIAGNOSIS": {
                        "type": ["string","null"],
                        "enum": ["SEEN", "NOT_SEEN"],
                    }
                },
                "required": ["VALUE", "DIAGNOSIS"],
                "additionalProperties": False
            },
             "URINE_BACTERIA": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type": ["string","null"]
                    },
                    "DIAGNOSIS": {
                        "type": ["string","null"],       
                        "enum": ["SEEN", "NOT_SEEN"],
                    }
                },
                "required": ["VALUE", "DIAGNOSIS"],
                "additionalProperties": False
            },
            "URINE_EPITHELIAL_CELLS": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type": ["string","null"]
                    },
                    "DIAGNOSIS": {
                        "type": ["string","null"],       
                        "enum": ["SEEN", "NOT_SEEN"],
                    }
                },
                "required": ["VALUE", "DIAGNOSIS"],
                "additionalProperties": False
            },
            "URINE_FAT_DROPLETS": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type": ["string","null"]
                    },
                    "DIAGNOSIS": {
                        "type": ["string","null"],
                        "enum": ["SEEN", "NOT_SEEN"],
                    }
                },
                "required": ["VALUE", "DIAGNOSIS"],
                "additionalProperties": False
            },
            "BLOOD_GAMMA_GLUTAMYL_TRANSFERASE_GGT": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type": ["number", "null"],
                    }
                },
                "required": ["VALUE"],
                "additionalProperties": False
            },
              "BLOOD_BILIRUBIN": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type": ["number", "null"],
                    }
                },
                "required": ["VALUE"],
                "additionalProperties": False
            },
            "BLOOD_MAGNESIUM": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type": ["number", "null"],
                    }
                },
                "required": ["VALUE"],
                "additionalProperties": False
            },
            "BLOOD_CHOLESTEROL": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type": ["number", "null"],
                    }
                },
                "required": ["VALUE"],
                "additionalProperties": False
            },
               "BLOOD_TRIGLYCERIDES": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type": ["number", "null"],
                    }
                },
                "required": ["VALUE"],
                "additionalProperties": False
            },
                "BLOOD_AMYLASE": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type": ["number", "null"],
                    }
                },
                "required": ["VALUE"],
                "additionalProperties": False
            },
             "BLOOD_PRECISION_PSL": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type": ["number", "null"],
                    }
                },
                "required": ["VALUE"],
                "additionalProperties": False
            },
             "BLOOD_HEMOGLOBIN_HGB": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type": ["number", "null"],
                    }
                },
                "required": ["VALUE"],
                "additionalProperties": False
            },
                "BLOOD_TOTAL_THYROXINE_T4": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type": ["number", "null"],
                    }
                },
                "required": ["VALUE"],
                "additionalProperties": False
            },

                "BLOOD_FREE_THYROXINE_T4": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type": ["number", "null"],
                    }
                },
                "required": ["VALUE"],
                "additionalProperties": False
            },
             "BLOOD_CREATINE_PHOSPHOKINASE_CPK": {
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type": ["number", "null"],
                    }
                },
                "required": ["VALUE"],
                "additionalProperties": False
            },
            "BLOOD_RED_CELL_DISTRIBUTION_WIDTH_RDW":{
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type": ["number", "null"],
                    }
                },
                "required": ["VALUE"],
                "additionalProperties": False
            },
              "SYSTOLIC_BLOOD_PRESSURE":{
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type": ["number", "null"],
                    },
                },
                "required": ["VALUE"],
                "additionalProperties": False
            },
             "DIASTOLIC_BLOOD_PRESSURE":{
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type": ["number", "null"],
                    },
                },
                "required": ["VALUE"],
                "additionalProperties": False
            },
              "BLOOD_RBC_HEALTH":{
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type": ["string", "null"],
                    },
                },
                "required": ["VALUE"],
                "additionalProperties": False
            },
              "URINE_URINARY_TRACT_INFECTION_UTI":{
                "type": "object",
                "properties": {
                    "VALUE": {
                        "type": ["string", "null"],
                        "enum": ["POSITIVE", "NEGATIVE"],
                    },
                },
                "required": ["VALUE"],
                "additionalProperties": False
            },
            "RENAL_TECH_PREDICTION":{
                "type":"object",
                "properties":{
                    "VALUE":{
                        "type":["string","null"]
                    }
                },
                "required":["VALUE"],
                "additionalProperties": False
            },
             "BLOOD_PH":{
                "type":"object",
                "properties":{
                    "VALUE":{
                        "type":["number","null"]
                    }
                },
                "required":["VALUE"],
                "additionalProperties": False
            },
              "BLOOD_ANION_GAP":{
                "type":"object",
                "properties":{
                    "VALUE":{
                        "type":["number","null"]
                    }
                },
                "required":["VALUE"],
                "additionalProperties": False
            },
               "BLOOD_BICARBONATE_HCO3":{
                "type":"object",
                "properties":{
                    "VALUE":{
                        "type":["number","null"]
                    }
                },
                "required":["VALUE"],
                "additionalProperties": False
            },
             "BLOOD_PARTIAL_PRESSSURE_OF_CARBONDIOXIDE_PCO2":{
                "type":"object",
                "properties":{
                    "VALUE":{
                        "type":["number","null"]
                    }
                },
                "required":["VALUE"],
                "additionalProperties": False
            },
               "BLOOD_PARTIAL_PRESSSURE_OF_OXYGEN_PO2":{
                "type":"object",
                "properties":{
                    "VALUE":{
                        "type":["number","null"]
                    }
                },
                "required":["VALUE"],
                "additionalProperties": False
            },
             "BLOOD_PLATELET_ESTIMATE":{
                "type":"object",
                "properties":{
                    "VALUE":{
                        "type":["string","null"]
                    }
                },
                "required":["VALUE"],
                "additionalProperties": False
            },
            "BLOOD_PARASITES":{
                "type":"object",
                "properties":{
                    "VALUE":{
                        "type":["string","null"]
                    }
                },
                "required":["VALUE"],
                "additionalProperties": False
            }, 
            "BLOOD_RBC_COMMENT":{
                "type":"object",
                "properties":{
                    "VALUE":{
                        "type":["string","null"]
                    }
                },
                "required":["VALUE"],
                "additionalProperties": False
            }, 
              "BLOOD_RETICULOCYTE_COUNT":{
                "type":"object",
                "properties":{
                    "VALUE":{
                        "type":["number","null"]
                    }
                },
                "required":["VALUE"],
                "additionalProperties": False
            }, 
              "BLOOD_RETICULOCYTE_PERCENTAGE":{
                "type":"object",
                "properties":{
                    "VALUE":{
                        "type":["number","null"]
                    }
                },
                "required":["VALUE"],
                "additionalProperties": False
            }
            ,
            "BLOOD_LIPASE":{
                "type":"object",
                "properties":{
                    "VALUE":{
                        "type":["number","null"]
                    }
                },
                "required":["VALUE"],
                "additionalProperties": False
            }, 

             "BLOOD_SERUM_IRON":{
                "type":"object",
                "properties":{
                    "VALUE":{
                        "type":["number","null"]
                    }
                },
                "required":["VALUE"],
                "additionalProperties": False
            }, 
             "BLOOD_FERRITIN":{
                "type":"object",
                "properties":{
                    "VALUE":{
                        "type":["number","null"]
                    }
                },
                "required":["VALUE"],
                "additionalProperties": False
            }, 
               "BLOOD_TOTAL_IRON_BINDING_CAPACITY_TIBC":{
                "type":"object",
                "properties":{
                    "VALUE":{
                        "type":["number","null"]
                    }
                },
                "required":["VALUE"],
                "additionalProperties": False
            }, 
               "BLOOD_TRANSFERRIN_SATURATION":{
                "type":"object",
                "properties":{
                    "VALUE":{
                        "type":["number","null"]
                    }
                },
                "required":["VALUE"],
                "additionalProperties": False
            }, 
            "BLOOD_ERYTHROPOIETIN_EPO":{
                "type":"object",
                "properties":{
                    "VALUE":{
                        "type":["number","null"]
                    }
                },
                "required":["VALUE"],
                "additionalProperties": False
            },
              "BLOOD_IONIZED_CALCIUM":{
                "type":"object",
                "properties":{
                    "VALUE":{
                        "type":["number","null"]
                    }
                },
                "required":["VALUE"],
                "additionalProperties": False
            },
                "BLOOD_PARATHYROID_HORMONE_PTH":{
                "type":"object",
                "properties":{
                    "VALUE":{
                        "type":["number","null"]
                    }
                },
                "required":["VALUE"],
                "additionalProperties": False
            },
              "BLOOD_VITAMIN_D_25HYDROXY":{
                "type":"object",
                "properties":{
                    "VALUE":{
                        "type":["number","null"]
                    }
                },
                "required":["VALUE"],
                "additionalProperties": False
            },
            
             "MEAN_ARTERIAL_PRESSURE_MAP":{
                "type":"object",
                "properties":{
                    "VALUE":{
                        "type":["number","null"]
                    }
                },
                "required":["VALUE"],
                "additionalProperties": False
            },
            "FUNDIC_EXAM":{
                "type":"object",
                "properties":{
                    "VALUE":{
                        "type":["string","null"]
                    }
                },
                "required":["VALUE"],
                "additionalProperties": False
            },
             "BLOOD_C_REACTIVE_PROTEIN":{
                "type":"object",
                "properties":{
                    "VALUE":{
                        "type":["string","null"]
                    }
                },
                "required":["VALUE"],
                "additionalProperties": False
            },
              "BLOOD_SERUM_AMYLOID_A_SAA":{
                "type":"object",
                "properties":{
                    "VALUE":{
                        "type":["string","null"]
                    }
                },
                "required":["VALUE"],
                "additionalProperties": False
            },
            "BLOOD_FIBRINOGEN":{
                "type":"object",
                "properties":{
                    "VALUE":{
                        "type":["string","null"]
                    }
                },
                "required":["VALUE"],
                "additionalProperties": False
            },
            "BODY_CONDITION_SCORE":{
                "type":"object",
                "properties":{
                    "VALUE":{
                        "type":["string","null"]
                    }
                },
                "required":["VALUE"],
                "additionalProperties": False
            },
             "MUSCLE_CONDITION_SCORE":{
                "type":"object",
                "properties":{
                    "VALUE":{
                        "type":["string","null"]
                    }
                },
                "required":["VALUE"],
                "additionalProperties": False
            },
              "URINE_MICRO_ALBUMINURIA":{
                "type":"object",
                "properties":{
                    "VALUE":{
                        "type":["number","null"]
                    }
                },
                "required":["VALUE"],
                "additionalProperties": False
            },
                "URINE_CULTURE_AND_SENSITIVITY":{
                "type":"object",
                "properties":{
                    "VALUE":{
                        "type":["string","null"]
                    }
                },
                "required":["VALUE"],
                "additionalProperties": False
            },

        },
        "required": ["NAME", "AGE", "GENDER","BLOOD_RETICULOCYTE_PERCENTAGE", "BREED", "WEIGHT","BLOOD_BICARBONATE_HCO3","URINE_CULTURE_AND_SENSITIVITY","URINE_MICRO_ALBUMINURIA","BLOOD_FREE_THYROXINE_T4","BODY_CONDITION_SCORE","BLOOD_FIBRINOGEN","MUSCLE_CONDITION_SCORE","BLOOD_SERUM_AMYLOID_A_SAA","BLOOD_C_REACTIVE_PROTEIN","FUNDIC_EXAM","MEAN_ARTERIAL_PRESSURE_MAP","BLOOD_VITAMIN_D_25HYDROXY","BLOOD_PARATHYROID_HORMONE_PTH","BLOOD_IONIZED_CALCIUM","BLOOD_ERYTHROPOIETIN_EPO","BLOOD_TRANSFERRIN_SATURATION","BLOOD_TOTAL_IRON_BINDING_CAPACITY_TIBC","BLOOD_FERRITIN","BLOOD_SERUM_IRON","BLOOD_RETICULOCYTE_COUNT","BLOOD_RBC_COMMENT","BLOOD_PARASITES","BLOOD_PLATELET_ESTIMATE","BLOOD_PARTIAL_PRESSSURE_OF_OXYGEN_PO2","BLOOD_PARTIAL_PRESSSURE_OF_CARBONDIOXIDE_PCO2","BLOOD_ANION_GAP","BLOOD_PH","RENAL_TECH_PREDICTION","BLOOD_RBC_HEALTH","SYSTOLIC_BLOOD_PRESSURE","DIASTOLIC_BLOOD_PRESSURE","BLOOD_RED_BLOOD_CELL_RBC","BLOOD_WHITE_BLOOD_CELL_WBC","BLOOD_RED_CELL_DISTRIBUTION_WIDTH_RDW","BLOOD_CREATINE_PHOSPHOKINASE_CPK","BLOOD_TOTAL_THYROXINE_T4","BLOOD_HEMOGLOBIN_HGB","BLOOD_PRECISION_PSL","BLOOD_AMYLASE","BLOOD_TRIGLYCERIDES","BLOOD_CHOLESTEROL","BLOOD_MAGNESIUM","BLOOD_BILIRUBIN","BLOOD_GAMMA_GLUTAMYL_TRANSFERASE_GGT", "BLOOD_TOTAL_PROTEIN", "BLOOD_UREA_NITROGEN_BUN", "BLOOD_ALBUMIN", "BLOOD_GLOBULIN", "BLOOD_HEMATOCRIT_HCT", "BLOOD_MEAN_CORPUSCULAR_VOLUME_MCV", "BLOOD_MEAN_CORPUSCULAR_HEMOGLOBIN_MCH","BLOOD_MEAN_CORPUSCULAR_HEMOGLOBIN_CONCENTRATION_MCHC", "BLOOD_BUN_CREATININE_RATIO","BLOOD_ALBUMIN_GLOBULIN_RATIO_AG","BLOOD_ALANINE_AMINOTRANSFERASE_ALT_SERUM_GLUTAMATE_PYRUVATE_TRANSFERASE_SGPT","BLOOD_CREATININE","BLOOD_ALKALINE_PHOSPHATE_ALP","URINE_URINARY_TRACT_INFECTION_UTI","BLOOD_LIPASE","BLOOD_GLUCOSE","BLOOD_SODIUM","BLOOD_POTASSIUM","BLOOD_SODIUM_POTASSIUM_RATIO_NAK","BLOOD_CHLORIDE","BLOOD_PLATELET_COUNT","BLOOD_NEUTROPHILS","BLOOD_LYMPHOCYTES","BLOOD_MONOCYTES","BLOOD_EOSINOPHILS","BLOOD_BASOPHILS","BLOOD_BANDS","URINE_COLLECTION_METHOD","URINE_COLOR","URINE_APPEARANCE","URINE_SPECIFIC_GRAVITY","URINE_PH","URINE_PROTEIN","URINE_GLUCOSE_STRIP","URINE_BILIRUBIN","URINE_KETONES","URINE_OCCULT_BLOOD","URINE_WHITE_BLOOD_CELL_WBC","URINE_RED_BLOOD_CELL_RBC","URINE_CASTS","URINE_CRYSTALS","URINE_BACTERIA","URINE_EPITHELIAL_CELLS","URINE_FAT_DROPLETS","BLOOD_SYMMETRIC_DIMETHYLARGININE_SDMA","BLOOD_PHOSPHORUS_PHOSPHATE","BLOOD_CALCIUM","BLOOD_ANAEMIA","URINE_PROTEIN_CREATININE_RATIO_UPC","BLOOD_ASPARTATE_AMINOTRANSFERASE_AST_SERUM_GLUTAMATE_OXALOACETATE_TRANSFERASE_SGOT"],
        "additionalProperties": False
    }