from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import re
from datetime import datetime
import random
import requests
from urllib.parse import quote

app = Flask(__name__)
CORS(app)

class MedicalChatbot:
    def __init__(self):
        self.medical_knowledge = {
            # Common symptoms and their possible conditions
            'symptoms': {
                'headache': {
                    'conditions': ['tension headache', 'migraine', 'dehydration', 'stress'],
                    'advice': 'Rest in a quiet, dark room. Stay hydrated. Consider over-the-counter pain relievers.',
                    'home_remedies': [
                        'Apply cold or warm compress to head/neck',
                        'Drink plenty of water to prevent dehydration',
                        'Practice deep breathing or meditation',
                        'Gentle neck and shoulder massage',
                        'Try peppermint or lavender essential oils'
                    ],
                    'medicines': [
                        {'name': 'Paracetamol 500mg', 'dosage': '1-2 tablets every 4-6 hours', 'tata1mg_link': 'https://www.1mg.com/drugs/paracetamol-500mg-tablet'},
                        {'name': 'Ibuprofen 400mg', 'dosage': '1 tablet every 6-8 hours', 'tata1mg_link': 'https://www.1mg.com/drugs/ibuprofen-400mg-tablet'},
                        {'name': 'Aspirin 325mg', 'dosage': '1-2 tablets every 4 hours', 'tata1mg_link': 'https://www.1mg.com/drugs/aspirin-325mg-tablet'}
                    ]
                },
                'fever': {
                    'conditions': ['viral infection', 'bacterial infection', 'flu'],
                    'advice': 'Rest, drink plenty of fluids, and monitor temperature. Seek medical care if fever exceeds 103°F.',
                    'home_remedies': [
                        'Drink plenty of fluids (water, herbal teas, clear broths)',
                        'Take lukewarm baths or use cool compresses',
                        'Wear light, breathable clothing',
                        'Get adequate rest and sleep',
                        'Eat light, easily digestible foods'
                    ],
                    'medicines': [
                        {'name': 'Paracetamol 500mg', 'dosage': '1-2 tablets every 4-6 hours', 'tata1mg_link': 'https://www.1mg.com/drugs/paracetamol-500mg-tablet'},
                        {'name': 'Ibuprofen 400mg', 'dosage': '1 tablet every 6-8 hours', 'tata1mg_link': 'https://www.1mg.com/drugs/ibuprofen-400mg-tablet'},
                        {'name': 'Crocin Advance 500mg', 'dosage': '1 tablet every 4-6 hours', 'tata1mg_link': 'https://www.1mg.com/drugs/crocin-advance-tablet'}
                    ]
                },
                'cough': {
                    'conditions': ['common cold', 'allergies', 'bronchitis', 'pneumonia'],
                    'advice': 'Stay hydrated, use a humidifier, avoid irritants. See a doctor if cough persists over 2 weeks.',
                    'home_remedies': [
                        'Drink warm water with honey and lemon',
                        'Use a humidifier or inhale steam',
                        'Gargle with warm salt water',
                        'Drink herbal teas (ginger, turmeric)',
                        'Avoid smoking and air pollutants'
                    ],
                    'medicines': [
                        {'name': 'Benadryl Cough Syrup', 'dosage': '5-10ml 3 times daily', 'tata1mg_link': 'https://www.1mg.com/drugs/benadryl-dr-cough-formula-syrup'},
                        {'name': 'Dextromethorphan 15mg', 'dosage': '1 tablet every 4 hours', 'tata1mg_link': 'https://www.1mg.com/drugs/dextromethorphan-tablet'},
                        {'name': 'Ambroxol 30mg', 'dosage': '1 tablet twice daily', 'tata1mg_link': 'https://www.1mg.com/drugs/ambroxol-30mg-tablet'}
                    ]
                },
                'stomach pain': {
                    'conditions': ['indigestion', 'gastritis', 'food poisoning', 'appendicitis'],
                    'advice': 'Avoid solid foods initially. Stay hydrated. Seek immediate care for severe pain.',
                    'home_remedies': [
                        'Drink warm water or herbal tea',
                        'Apply warm compress to abdomen',
                        'Try ginger tea for nausea',
                        'Eat bland foods (rice, toast, bananas)',
                        'Practice gentle abdominal massage'
                    ],
                    'medicines': [
                        {'name': 'Eno Fruit Salt', 'dosage': '1 sachet in water when needed', 'tata1mg_link': 'https://www.1mg.com/drugs/eno-fruit-salt'},
                        {'name': 'Omeprazole 20mg', 'dosage': '1 capsule daily before breakfast', 'tata1mg_link': 'https://www.1mg.com/drugs/omeprazole-20mg-capsule'},
                        {'name': 'Digene Antacid', 'dosage': '1-2 tablets after meals', 'tata1mg_link': 'https://www.1mg.com/drugs/digene-antacid-tablet'}
                    ]
                },
                'chest pain': {
                    'conditions': ['muscle strain', 'acid reflux', 'anxiety', 'heart condition'],
                    'advice': 'IMPORTANT: Seek immediate medical attention for any chest pain, especially if accompanied by shortness of breath.',
                    'home_remedies': [
                        'CAUTION: Chest pain requires immediate medical attention',
                        'If cleared by doctor - gentle stretching for muscle strain',
                        'Deep breathing exercises for anxiety',
                        'Avoid heavy meals if due to acid reflux'
                    ],
                    'medicines': [
                        {'name': 'Emergency Care Required', 'dosage': 'Call 911 immediately', 'tata1mg_link': 'https://www.1mg.com/emergency-care'}
                    ]
                },
                'cold': {
                    'conditions': ['viral infection', 'common cold', 'seasonal allergies'],
                    'advice': 'Rest, stay hydrated, and use supportive care. Most colds resolve in 7-10 days.',
                    'home_remedies': [
                        'Drink warm fluids (tea, soup, warm water)',
                        'Use saline nasal rinses or drops',
                        'Gargle with warm salt water',
                        'Get plenty of rest',
                        'Use a humidifier in your room'
                    ],
                    'medicines': [
                        {'name': 'Cetirizine 10mg', 'dosage': '1 tablet daily', 'tata1mg_link': 'https://www.1mg.com/drugs/cetirizine-10mg-tablet'},
                        {'name': 'Paracetamol + Phenylephrine', 'dosage': '1 tablet every 6 hours', 'tata1mg_link': 'https://www.1mg.com/drugs/dolo-cold-tablet'},
                        {'name': 'Vicks Vaporub', 'dosage': 'Apply on chest/back', 'tata1mg_link': 'https://www.1mg.com/drugs/vicks-vaporub'}
                    ]
                },
                'back pain': {
                    'conditions': ['muscle strain', 'poor posture', 'herniated disc', 'arthritis'],
                    'advice': 'Apply ice for acute pain, then heat after 48 hours. Gentle stretching and movement.',
                    'home_remedies': [
                        'Apply ice pack for 15-20 minutes',
                        'Use heating pad after 48 hours',
                        'Gentle stretching exercises',
                        'Maintain good posture',
                        'Sleep on firm mattress'
                    ],
                    'medicines': [
                        {'name': 'Ibuprofen 400mg', 'dosage': '1 tablet every 6-8 hours', 'tata1mg_link': 'https://www.1mg.com/drugs/ibuprofen-400mg-tablet'},
                        {'name': 'Diclofenac Gel', 'dosage': 'Apply 2-3 times daily', 'tata1mg_link': 'https://www.1mg.com/drugs/diclofenac-gel'},
                        {'name': 'Muscle relaxant', 'dosage': 'As prescribed by doctor', 'tata1mg_link': 'https://www.1mg.com/search/all?name=muscle%20relaxant'}
                    ]
                },
                'sore throat': {
                    'conditions': ['viral infection', 'bacterial infection', 'allergies', 'dry air'],
                    'advice': 'Gargle with salt water, stay hydrated, and rest your voice.',
                    'home_remedies': [
                        'Gargle with warm salt water',
                        'Drink warm tea with honey',
                        'Suck on throat lozenges',
                        'Use a humidifier',
                        'Rest your voice'
                    ],
                    'medicines': [
                        {'name': 'Strepsils Lozenges', 'dosage': '1 lozenge every 2-3 hours', 'tata1mg_link': 'https://www.1mg.com/drugs/strepsils-lozenges'},
                        {'name': 'Betadine Gargle', 'dosage': 'Gargle 3-4 times daily', 'tata1mg_link': 'https://www.1mg.com/drugs/betadine-gargle'},
                        {'name': 'Paracetamol 500mg', 'dosage': '1-2 tablets every 4-6 hours', 'tata1mg_link': 'https://www.1mg.com/drugs/paracetamol-500mg-tablet'}
                    ]
                },
                'nausea': {
                    'conditions': ['motion sickness', 'food poisoning', 'pregnancy', 'migraine'],
                    'advice': 'Rest, small sips of clear fluids, avoid strong smells.',
                    'home_remedies': [
                        'Drink ginger tea',
                        'Eat small, frequent meals',
                        'Try crackers or toast',
                        'Get fresh air',
                        'Rest in a cool, quiet place'
                    ],
                    'medicines': [
                        {'name': 'Domperidone 10mg', 'dosage': '1 tablet before meals', 'tata1mg_link': 'https://www.1mg.com/drugs/domperidone-10mg-tablet'},
                        {'name': 'Ondem 4mg', 'dosage': '1 tablet as needed', 'tata1mg_link': 'https://www.1mg.com/drugs/ondem-4mg-tablet'},
                        {'name': 'Ginger capsules', 'dosage': '1-2 capsules daily', 'tata1mg_link': 'https://www.1mg.com/search/all?name=ginger%20capsules'}
                    ]
                },
                'diarrhea': {
                    'conditions': ['food poisoning', 'viral infection', 'bacteria', 'stress'],
                    'advice': 'Stay hydrated with ORS, eat bland foods, rest.',
                    'home_remedies': [
                        'Drink ORS (oral rehydration solution)',
                        'Eat BRAT diet (banana, rice, apple, toast)',
                        'Drink plenty of fluids',
                        'Avoid dairy and fatty foods',
                        'Rest and avoid stress'
                    ],
                    'medicines': [
                        {'name': 'ORS Packets', 'dosage': '1 packet in 1 liter water', 'tata1mg_link': 'https://www.1mg.com/drugs/ors-packets'},
                        {'name': 'Loperamide 2mg', 'dosage': '1 tablet after each loose stool', 'tata1mg_link': 'https://www.1mg.com/drugs/loperamide-2mg-tablet'},
                        {'name': 'Probiotic capsules', 'dosage': '1-2 capsules daily', 'tata1mg_link': 'https://www.1mg.com/search/all?name=probiotic'}
                    ]
                },
                'constipation': {
                    'conditions': ['low fiber diet', 'dehydration', 'lack of exercise', 'medication side effects'],
                    'advice': 'Increase fiber intake, drink more water, exercise regularly.',
                    'home_remedies': [
                        'Drink more water (8-10 glasses daily)',
                        'Eat high-fiber foods',
                        'Exercise regularly',
                        'Try prunes or prune juice',
                        'Establish regular bathroom routine'
                    ],
                    'medicines': [
                        {'name': 'Isabgol (Psyllium)', 'dosage': '1-2 tsp with water daily', 'tata1mg_link': 'https://www.1mg.com/drugs/isabgol-psyllium'},
                        {'name': 'Lactulose syrup', 'dosage': '15-30ml daily', 'tata1mg_link': 'https://www.1mg.com/drugs/lactulose-syrup'},
                        {'name': 'Fiber supplements', 'dosage': 'As per package instructions', 'tata1mg_link': 'https://www.1mg.com/search/all?name=fiber%20supplements'}
                    ]
                },
                'insomnia': {
                    'conditions': ['stress', 'anxiety', 'poor sleep hygiene', 'caffeine'],
                    'advice': 'Maintain regular sleep schedule, create relaxing bedtime routine.',
                    'home_remedies': [
                        'Maintain regular sleep schedule',
                        'Avoid caffeine after 2 PM',
                        'Create dark, cool sleeping environment',
                        'Try relaxation techniques',
                        'Limit screen time before bed'
                    ],
                    'medicines': [
                        {'name': 'Melatonin 3mg', 'dosage': '1 tablet 30 minutes before bed', 'tata1mg_link': 'https://www.1mg.com/drugs/melatonin-3mg-tablet'},
                        {'name': 'Ashwagandha capsules', 'dosage': '1-2 capsules before bed', 'tata1mg_link': 'https://www.1mg.com/search/all?name=ashwagandha'},
                        {'name': 'Chamomile tea', 'dosage': '1 cup before bedtime', 'tata1mg_link': 'https://www.1mg.com/search/all?name=chamomile%20tea'}
                    ]
                },
                'anxiety': {
                    'conditions': ['stress', 'work pressure', 'life changes', 'health concerns'],
                    'advice': 'Practice relaxation techniques, maintain regular routine, seek support if needed.',
                    'home_remedies': [
                        'Practice deep breathing exercises',
                        'Try meditation or mindfulness',
                        'Regular physical exercise',
                        'Maintain social connections',
                        'Limit caffeine and alcohol'
                    ],
                    'medicines': [
                        {'name': 'Ashwagandha tablets', 'dosage': '1-2 tablets daily', 'tata1mg_link': 'https://www.1mg.com/search/all?name=ashwagandha'},
                        {'name': 'Brahmi capsules', 'dosage': '1 capsule twice daily', 'tata1mg_link': 'https://www.1mg.com/search/all?name=brahmi'},
                        {'name': 'Consultation required', 'dosage': 'See doctor for prescription', 'tata1mg_link': 'https://www.1mg.com/online-doctor-consultation'}
                    ]
                },
                'allergies': {
                    'conditions': ['seasonal allergies', 'food allergies', 'dust mites', 'pet dander'],
                    'advice': 'Identify and avoid triggers, use antihistamines as needed.',
                    'home_remedies': [
                        'Avoid known allergens',
                        'Use air purifiers',
                        'Wash bedding in hot water',
                        'Keep windows closed during high pollen days',
                        'Rinse nasal passages with saline'
                    ],
                    'medicines': [
                        {'name': 'Cetirizine 10mg', 'dosage': '1 tablet daily', 'tata1mg_link': 'https://www.1mg.com/drugs/cetirizine-10mg-tablet'},
                        {'name': 'Loratadine 10mg', 'dosage': '1 tablet daily', 'tata1mg_link': 'https://www.1mg.com/drugs/loratadine-10mg-tablet'},
                        {'name': 'Nasal spray', 'dosage': '1-2 sprays per nostril', 'tata1mg_link': 'https://www.1mg.com/search/all?name=nasal%20spray'}
                    ]
                },
                'acidity': {
                    'conditions': ['gastroesophageal reflux', 'spicy food', 'stress', 'irregular eating'],
                    'advice': 'Avoid spicy foods, eat smaller meals, dont lie down after eating.',
                    'home_remedies': [
                        'Eat smaller, frequent meals',
                        'Avoid spicy and fatty foods',
                        'Dont lie down immediately after eating',
                        'Drink plenty of water',
                        'Try cold milk or banana'
                    ],
                    'medicines': [
                        {'name': 'Omeprazole 20mg', 'dosage': '1 capsule before breakfast', 'tata1mg_link': 'https://www.1mg.com/drugs/omeprazole-20mg-capsule'},
                        {'name': 'Ranitidine 150mg', 'dosage': '1 tablet twice daily', 'tata1mg_link': 'https://www.1mg.com/drugs/ranitidine-150mg-tablet'},
                        {'name': 'Antacid syrup', 'dosage': '10-15ml after meals', 'tata1mg_link': 'https://www.1mg.com/search/all?name=antacid%20syrup'}
                    ]
                }
            },
            # General health tips
            'health_tips': [
                'Drink at least 8 glasses of water daily for optimal hydration.',
                'Aim for 7-9 hours of sleep each night for better health.',
                'Exercise regularly - even 30 minutes of walking daily helps.',
                'Eat a balanced diet rich in fruits and vegetables.',
                'Wash your hands frequently to prevent infections.',
                'Schedule regular check-ups with your healthcare provider.'
            ],
            # Emergency symptoms
            'emergency_symptoms': [
                'severe chest pain', 'difficulty breathing', 'severe allergic reaction',
                'loss of consciousness', 'severe bleeding', 'signs of stroke',
                'severe abdominal pain', 'high fever with stiff neck'
            ],
            # Country-specific emergency information
            'emergency_numbers': {
                'india': {
                    'emergency_services': '112 (National Emergency Number)',
                    'police': '100',
                    'fire': '101',
                    'ambulance': '108',
                    'women_helpline': '1091',
                    'child_helpline': '1098',
                    'disaster_management': '1070',
                    'tourist_helpline': '1363',
                    'poison_control': '011-26589391',
                    'mental_health': '9152987821 (COOJ Mental Health Foundation)'
                },
                'usa': {
                    'emergency_services': '911',
                    'poison_control': '1-800-222-1222',
                    'suicide_prevention': '988',
                    'domestic_violence': '1-800-799-7233',
                    'mental_health': '1-800-950-6264',
                    'substance_abuse': '1-800-662-4357'
                },
                'uk': {
                    'emergency_services': '999',
                    'non_emergency_police': '101',
                    'non_emergency_medical': '111',
                    'samaritans': '116 123',
                    'domestic_violence': '0808 2000 247',
                    'childline': '0800 1111'
                },
                'canada': {
                    'emergency_services': '911',
                    'poison_control': '1-844-764-7669',
                    'mental_health': '1-833-456-4566',
                    'kids_help_phone': '1-800-668-6868'
                },
                'australia': {
                    'emergency_services': '000',
                    'police_assistance': '131 444',
                    'poison_information': '13 11 26',
                    'lifeline': '13 11 14',
                    'kids_helpline': '1800 55 1800'
                },
                'germany': {
                    'emergency_services': '112',
                    'police': '110',
                    'poison_control': '+49 30 19240',
                    'telephone_counseling': '0800 111 0 111'
                },
                'default': {
                    'emergency_services': '112 (European Emergency Number)',
                    'note': 'Emergency numbers vary by country. Please look up local emergency numbers for your area.'
                }
            },
            # Nation-specific traditional remedies
            'traditional_remedies': {
                'india': {
                    'headache': ['Drink ginger tea', 'Apply sandalwood paste on forehead', 'Massage with coconut oil'],
                    'fever': ['Drink tulsi (holy basil) tea', 'Use neem leaves paste', 'Drink turmeric milk'],
                    'cough': ['Honey with black pepper', 'Ginger-honey-lemon tea', 'Turmeric with warm milk'],
                    'cold': ['Steam inhalation with ajwain', 'Kadha (herbal decoction)', 'Garlic-honey mixture'],
                    'stomach pain': ['Jeera (cumin) water', 'Hing (asafoetida) with warm water', 'Ginger tea'],
                    'back pain': ['Apply warm mustard oil massage', 'Use turmeric paste', 'Try yoga poses'],
                    'sore throat': ['Gargle with turmeric-salt water', 'Honey with ginger', 'Tulsi leaves tea'],
                    'nausea': ['Ginger tea', 'Lemon water', 'Mint leaves'],
                    'diarrhea': ['Drink buttermilk', 'Eat curd rice', 'Pomegranate juice'],
                    'constipation': ['Drink warm water with lemon', 'Eat papaya', 'Isabgol with water'],
                    'insomnia': ['Drink warm milk with turmeric', 'Meditation', 'Brahmi tea'],
                    'anxiety': ['Practice pranayama', 'Ashwagandha powder', 'Brahmi leaves'],
                    'allergies': ['Neem leaves paste', 'Turmeric milk', 'Avoid allergens'],
                    'acidity': ['Drink cold milk', 'Eat banana', 'Fennel seeds after meals']
                },
                'usa': {
                    'headache': ['Peppermint oil on temples', 'Cold compress', 'Chamomile tea'],
                    'fever': ['Elderberry syrup', 'Willow bark tea', 'Cool baths'],
                    'cough': ['Honey and lemon', 'Licorice root tea', 'Marshmallow root'],
                    'cold': ['Echinacea tea', 'Zinc supplements', 'Chicken soup'],
                    'stomach pain': ['Ginger ale', 'BRAT diet', 'Peppermint tea']
                },
                'uk': {
                    'headache': ['Lavender oil', 'Feverfew tea', 'Rosemary tea'],
                    'fever': ['Elderflower tea', 'Willow bark', 'Cool compress'],
                    'cough': ['Thyme tea', 'Honey and lemon', 'Steam inhalation'],
                    'cold': ['Lemon and honey', 'Ginger tea', 'Garlic'],
                    'stomach pain': ['Chamomile tea', 'Fennel tea', 'Ginger biscuits']
                },
                'china': {
                    'headache': ['Green tea', 'Ginkgo biloba', 'Acupressure'],
                    'fever': ['Chrysanthemum tea', 'White willow bark', 'Cooling foods'],
                    'cough': ['Pear soup', 'Fritillaria bulb', 'Loquat leaf tea'],
                    'cold': ['Ginger tea', 'Scallion white tea', 'Honeysuckle tea'],
                    'stomach pain': ['Hawthorn tea', 'Licorice root', 'Warm rice porridge']
                },
                'germany': {
                    'headache': ['Peppermint tea', 'Chamomile compress', 'Willow bark'],
                    'fever': ['Linden flower tea', 'Elder flower', 'Cool wraps'],
                    'cough': ['Sage tea', 'Thyme syrup', 'Pine needle tea'],
                    'cold': ['Camomile tea', 'Eucalyptus steam', 'Ginger tea'],
                    'stomach pain': ['Fennel tea', 'Caraway seeds', 'Chamomile tea']
                }
            }
        }
        
        self.conversation_history = []
        self.user_location = None
        self.user_country = None
        
        # Symptom synonyms and variations for better detection
        self.symptom_synonyms = {
            'headache': ['headache', 'head pain', 'migraine', 'head ache', 'head hurts', 'cranial pain'],
            'fever': ['fever', 'high temperature', 'hot', 'burning up', 'pyrexia', 'temperature'],
            'cough': ['cough', 'coughing', 'hack', 'phlegm', 'throat irritation'],
            'stomach pain': ['stomach pain', 'stomach ache', 'belly pain', 'abdominal pain', 'tummy ache', 'gastric pain', 'stomach hurts'],
            'chest pain': ['chest pain', 'chest ache', 'heart pain', 'chest discomfort', 'chest tightness'],
            'cold': ['cold', 'running nose', 'stuffy nose', 'sneezing', 'nasal congestion', 'runny nose'],
            'back pain': ['back pain', 'backache', 'lower back pain', 'spine pain', 'back hurts', 'lumbar pain'],
            'sore throat': ['sore throat', 'throat pain', 'throat ache', 'throat irritation', 'scratchy throat'],
            'nausea': ['nausea', 'feeling sick', 'queasy', 'nauseated', 'vomiting', 'throw up', 'morning sickness'],
            'diarrhea': ['diarrhea', 'loose stool', 'watery stool', 'frequent stool', 'loose motion', 'upset stomach'],
            'constipation': ['constipation', 'hard stool', 'difficulty passing stool', 'blocked', 'not able to pass stool'],
            'insomnia': ['insomnia', 'sleeplessness', 'cannot sleep', 'difficulty sleeping', 'sleep problems', 'no sleep'],
            'anxiety': ['anxiety', 'anxious', 'worried', 'stress', 'tension', 'panic', 'nervous', 'restless'],
            'allergies': ['allergies', 'allergic reaction', 'itching', 'rash', 'hives', 'sneezing', 'watery eyes'],
            'acidity': ['acidity', 'heartburn', 'acid reflux', 'burning sensation', 'gastric problem', 'sour taste']
        }
    
    def analyze_symptoms(self, user_input):
        """Analyze user input for symptoms and provide relevant information"""
        user_input_lower = user_input.lower()
        
        # Check for emergency symptoms
        for emergency in self.medical_knowledge['emergency_symptoms']:
            if emergency in user_input_lower:
                return {
                    'type': 'emergency',
                    'message': f"⚠️ EMERGENCY: If you're experiencing {emergency}, please call emergency services (911) immediately or go to the nearest emergency room.",
                    'severity': 'high'
                }
        
        # Check for known symptoms using synonyms
        found_symptoms = []
        for symptom, synonyms in self.symptom_synonyms.items():
            for synonym in synonyms:
                if synonym in user_input_lower:
                    if symptom not in found_symptoms:
                        found_symptoms.append(symptom)
                    break
        
        if found_symptoms:
            response = "Based on your symptoms, here's what I found:\n\n"
            for symptom in found_symptoms:
                symptom_info = self.medical_knowledge['symptoms'][symptom]
                response += f"**{symptom.title()}:**\n"
                response += f"Possible conditions: {', '.join(symptom_info['conditions'])}\n"
                response += f"General advice: {symptom_info['advice']}\n\n"
                
                # Add home remedies
                if 'home_remedies' in symptom_info:
                    response += "**🏠 General Home Remedies:**\n"
                    for remedy in symptom_info['home_remedies']:
                        response += f"• {remedy}\n"
                    response += "\n"
                
                # Add traditional remedies based on location
                traditional_remedies = self.get_traditional_remedies(symptom)
                if traditional_remedies:
                    country_name = self.user_location['country'] if self.user_location else 'your region'
                    response += f"**🌍 Traditional Remedies ({country_name}):**\n"
                    for remedy in traditional_remedies:
                        response += f"• {remedy}\n"
                    response += "\n"
                
                # Add medicine suggestions with multiple pharmacy options
                if 'medicines' in symptom_info:
                    response += "**💊 Medicine Suggestions:**\n"
                    for medicine in symptom_info['medicines']:
                        response += f"• **{medicine['name']}** - {medicine['dosage']}\n"
                        
                        # Get online search results for this medicine
                        search_results = self.search_medicine_online(medicine['name'])
                        if search_results:
                            response += "  🛒 **Online Pharmacies:**\n"
                            for pharmacy, url in search_results.items():
                                pharmacy_name = pharmacy.replace('_', ' ').title()
                                response += f"    • {pharmacy_name}: {url}\n"
                        response += "\n"
            
            response += "⚠️ **Important:** This information is for educational purposes only. Please consult with a healthcare professional for proper diagnosis and treatment. Always read medicine labels and follow dosage instructions."
            
            return {
                'type': 'symptom_analysis',
                'message': response,
                'medicines': [med for symptom in found_symptoms for med in self.medical_knowledge['symptoms'][symptom].get('medicines', [])],
                'remedies': [remedy for symptom in found_symptoms for remedy in self.medical_knowledge['symptoms'][symptom].get('home_remedies', [])],
                'severity': 'medium'
            }
        
        return None
    
    def get_health_tip(self):
        """Return a random health tip"""
        return random.choice(self.medical_knowledge['health_tips'])
    
    def get_user_location_from_ip(self, ip_address):
        """Get user location from IP address"""
        try:
            # Using ipapi.co for IP geolocation with SSL verification disabled
            import ssl
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            
            response = requests.get(f'https://ipapi.co/{ip_address}/json/', timeout=5, verify=False)
            if response.status_code == 200:
                data = response.json()
                self.user_location = {
                    'city': data.get('city', 'Unknown'),
                    'region': data.get('region', 'Unknown'),
                    'country': data.get('country_name', 'Unknown'),
                    'country_code': data.get('country_code', 'Unknown').lower(),
                    'latitude': data.get('latitude'),
                    'longitude': data.get('longitude')
                }
                self.user_country = data.get('country_code', 'Unknown').lower()
                print(f"Location detected: {self.user_location}")
                return self.user_location
        except Exception as e:
            print(f"Location detection error: {e}")
            # Fallback to alternative location service
            try:
                response = requests.get(f'http://ip-api.com/json/{ip_address}', timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    if data.get('status') == 'success':
                        self.user_location = {
                            'city': data.get('city', 'Unknown'),
                            'region': data.get('regionName', 'Unknown'),
                            'country': data.get('country', 'Unknown'),
                            'country_code': data.get('countryCode', 'Unknown').lower(),
                            'latitude': data.get('lat'),
                            'longitude': data.get('lon')
                        }
                        self.user_country = data.get('countryCode', 'Unknown').lower()
                        print(f"Fallback location detected: {self.user_location}")
                        return self.user_location
            except Exception as e2:
                print(f"Fallback location detection error: {e2}")
        return None
    
    def get_traditional_remedies(self, symptom, country=None):
        """Get traditional remedies based on country"""
        if not country:
            country = self.user_country or 'usa'  # Default to USA
        
        traditional_remedies = self.medical_knowledge['traditional_remedies']
        if country in traditional_remedies and symptom in traditional_remedies[country]:
            return traditional_remedies[country][symptom]
        elif 'usa' in traditional_remedies and symptom in traditional_remedies['usa']:
            return traditional_remedies['usa'][symptom]  # Fallback to USA remedies
        return []
    
    def search_medicine_online(self, medicine_name):
        """Search for medicine information online"""
        try:
            # Create search URLs for different pharmacy websites
            search_results = {
                'tata_1mg': f"https://www.1mg.com/search/all?name={quote(medicine_name)}",
                'netmeds': f"https://www.netmeds.com/catalogsearch/result/{quote(medicine_name)}/all",
                'pharmeasy': f"https://pharmeasy.in/search/all?name={quote(medicine_name)}",
                'apollo': f"https://www.apollopharmacy.in/search-medicines/{quote(medicine_name)}",
                'medicine_info': f"https://www.drugs.com/search.php?searchterm={quote(medicine_name)}"
            }
            return search_results
        except Exception as e:
            print(f"Medicine search error: {e}")
            return {}
    
    def find_nearby_hospitals(self, latitude, longitude, radius=5000):
        """Generate Google Maps search URL for nearby hospitals"""
        try:
            if latitude and longitude:
                # Create Google Maps search URL for hospitals
                maps_url = f"https://www.google.com/maps/search/hospitals+near+{latitude},{longitude}/@{latitude},{longitude},{radius}m"
                return {
                    'maps_url': maps_url,
                    'search_query': f"hospitals near {latitude},{longitude}",
                    'radius_meters': radius
                }
        except Exception as e:
            print(f"Hospital search error: {e}")
        return {}
    
    def get_emergency_info_by_country(self, country=None):
        """Get emergency information based on country"""
        if not country:
            country = self.user_country or 'default'
        
        emergency_numbers = self.medical_knowledge['emergency_numbers']
        
        if country in emergency_numbers:
            return emergency_numbers[country]
        elif country in ['us', 'united states']:
            return emergency_numbers['usa']
        elif country in ['in', 'ind']:
            return emergency_numbers['india']
        elif country in ['gb', 'england', 'scotland', 'wales']:
            return emergency_numbers['uk']
        elif country in ['de', 'deutschland']:
            return emergency_numbers['germany']
        elif country in ['ca']:
            return emergency_numbers['canada']
        elif country in ['au']:
            return emergency_numbers['australia']
        else:
            return emergency_numbers['default']
    
    def get_response(self, user_input):
        """Generate response based on user input"""
        user_input_lower = user_input.lower()
        
        # Store conversation
        self.conversation_history.append({
            'user': user_input,
            'timestamp': datetime.now().isoformat()
        })
        
        # Check for greetings
        if any(greeting in user_input_lower for greeting in ['hello', 'hi', 'hey', 'good morning', 'good afternoon']):
            response = "Hello! I'm your medical assistant chatbot. I can help you with:\n\n• Basic symptom information\n• General health advice\n• Health tips\n• When to seek medical care\n\nHow can I assist you today? Please describe any symptoms or health questions you have."
        
        # Check for symptom analysis with expanded keywords
        elif any(word in user_input_lower for word in ['pain', 'hurt', 'ache', 'fever', 'cough', 'sick', 'symptom', 'feel', 'feeling', 'nausea', 'tired', 'weak', 'dizzy', 'anxious', 'stressed', 'worried', 'sleep', 'insomnia', 'headache', 'stomach', 'throat', 'back', 'chest', 'cold', 'allergy', 'rash', 'itch', 'burn', 'sore', 'diarrhea', 'constipation', 'acidity', 'heartburn', 'loose', 'motion', 'stool', 'bowel', 'vomit', 'throw']):
            symptom_analysis = self.analyze_symptoms(user_input)
            if symptom_analysis:
                response = symptom_analysis['message']
            else:
                response = "I understand you're not feeling well. Could you please provide more specific details about your symptoms? For example:\n• Where do you feel pain?\n• How long have you had these symptoms?\n• How severe is the discomfort (1-10 scale)?\n\nThis will help me provide better guidance.\n\n**I can help with:**\n• Headache, fever, cough, cold\n• Back pain, stomach pain, sore throat\n• Nausea, diarrhea, constipation\n• Insomnia, anxiety, allergies\n• Acidity and many more conditions"
        
        # Check for remedy requests
        elif any(word in user_input_lower for word in ['remedy', 'remedies', 'home remedy', 'natural', 'cure']):
            found_symptoms = []
            for symptom in self.medical_knowledge['symptoms']:
                if symptom in user_input_lower:
                    found_symptoms.append(symptom)
            
            if found_symptoms:
                response = "Here are some natural home remedies you can try:\n\n"
                for symptom in found_symptoms:
                    symptom_info = self.medical_knowledge['symptoms'][symptom]
                    remedies = symptom_info.get('home_remedies', [])
                    if remedies:
                        response += f"**🏠 For {symptom.title()}:**\n"
                        for remedy in remedies:
                            response += f"• {remedy}\n"
                        response += "\n"
                
                response += "⚠️ **Note:** These are general home remedies. If symptoms persist or worsen, please consult a healthcare professional."
            else:
                response = "I can suggest home remedies for common conditions like:\n\n• Headache\n• Fever\n• Cough\n• Cold\n• Stomach pain\n\nPlease specify your symptoms, and I'll provide natural remedies you can try at home."
        
        # Check for health tips request
        elif any(word in user_input_lower for word in ['tip', 'advice', 'healthy', 'wellness', 'prevention']):
            response = f"Here's a health tip for you:\n\n💡 {self.get_health_tip()}\n\nWould you like more health information or do you have specific health questions?"
        
        # Check for emergency or urgent care questions
        elif any(word in user_input_lower for word in ['emergency', 'urgent', 'ambulance', 'hospital emergency', 'emergency room']):
            emergency_info = self.get_emergency_info_by_country()
            location_text = f" in {self.user_location['country']}" if self.user_location else ""
            
            response = f"🚨 **EMERGENCY INFORMATION{location_text.upper()}**\n\n"
            response += f"**Emergency Services:** {emergency_info.get('emergency_services', '112')}\n"
            
            # Add country-specific numbers
            for key, value in emergency_info.items():
                if key != 'emergency_services' and key != 'note':
                    formatted_key = key.replace('_', ' ').title()
                    response += f"**{formatted_key}:** {value}\n"
            
            response += f"\n⚠️ **Call {emergency_info.get('emergency_services', '112')} immediately for life-threatening emergencies!**"
        
        # Check for appointment or doctor questions  
        elif any(word in user_input_lower for word in ['doctor', 'appointment', 'see', 'visit', 'hospital']):
            emergency_info = self.get_emergency_info_by_country()
            response = "I recommend consulting with a healthcare professional when:\n\n• Symptoms persist or worsen\n• You experience severe pain\n• You have concerns about your health\n• You need a proper diagnosis\n• You need prescription medication\n\nFor non-emergency situations, you can:\n• Contact your primary care physician\n• Use telehealth services\n• Visit an urgent care clinic\n\n"
            response += f"For emergencies, call {emergency_info.get('emergency_services', '112')} immediately."
        
        # Check for medication questions
        elif any(word in user_input_lower for word in ['medicine', 'medication', 'drug', 'pill', 'treatment']):
            # Check if asking about specific symptoms
            found_symptoms = []
            for symptom in self.medical_knowledge['symptoms']:
                if symptom in user_input_lower:
                    found_symptoms.append(symptom)
            
            if found_symptoms:
                response = "Here are some over-the-counter medicine suggestions:\n\n"
                for symptom in found_symptoms:
                    symptom_info = self.medical_knowledge['symptoms'][symptom]
                    medicines = symptom_info.get('medicines', [])
                    if medicines:
                        response += f"**For {symptom.title()}:**\n"
                        for medicine in medicines:
                            response += f"• **{medicine['name']}** - {medicine['dosage']}\n"
                            response += f"  🛒 Order on Tata 1mg: {medicine['tata1mg_link']}\n"
                        response += "\n"
                
                response += "⚠️ **Important:** Always consult with a healthcare professional before taking any medication. Read labels carefully and follow dosage instructions."
            else:
                response = "I can provide over-the-counter medicine suggestions for common symptoms like:\n\n• Headache\n• Fever\n• Cough\n• Cold\n• Stomach pain\n\nPlease specify your symptoms, and I'll suggest appropriate medicines with Tata 1mg links.\n\n⚠️ **Important:** For prescription medications or serious conditions, please consult your healthcare provider."
        
        # General health questions
        elif any(word in user_input_lower for word in ['what', 'how', 'why', 'when', 'should']):
            response = "I'd be happy to help with general health information! Could you please be more specific about your question? I can provide guidance on:\n\n• Common symptoms and conditions\n• General health and wellness tips\n• When to seek medical care\n• Healthy lifestyle recommendations\n\nWhat specific health topic would you like to know about?"
        
        # Default response
        else:
            response = "I'm here to help with your health questions! I can assist with:\n\n• Symptom information\n• General health advice\n• Wellness tips\n• Guidance on when to seek medical care\n\nPlease feel free to ask me about any health concerns you have, or type 'health tip' for a wellness suggestion."
        
        # Add timestamp to conversation history
        self.conversation_history[-1]['bot_response'] = response
        
        return response

# Initialize chatbot
chatbot = MedicalChatbot()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Get user IP for location detection
        user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        if user_ip and not chatbot.user_location:
            location_result = chatbot.get_user_location_from_ip(user_ip)
            print(f"Chat endpoint - Location detection result: {location_result}")
            print(f"Chat endpoint - User country: {chatbot.user_country}")
        
        response = chatbot.get_response(user_message)
        
        return jsonify({
            'response': response,
            'user_location': chatbot.user_location,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health-tip', methods=['GET'])
def health_tip():
    try:
        tip = chatbot.get_health_tip()
        return jsonify({
            'tip': tip,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/emergency-info', methods=['GET'])
def emergency_info():
    try:
        # Get user IP for auto-detection
        user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        
        # Try to detect location if not already detected
        if not chatbot.user_location and user_ip:
            chatbot.get_user_location_from_ip(user_ip)
        
        # Get country from query parameter or detected location
        country = request.args.get('country')
        if not country:
            country = chatbot.user_country
        
        # If still no country detected, try to detect from headers or IP
        if not country or country == 'unknown':
            # Check if running locally or specific IP ranges
            if user_ip in ['127.0.0.1', 'localhost', '::1']:
                # Running locally - default to India as requested by user
                country = 'india'
                chatbot.user_country = 'india'
                chatbot.user_location = {
                    'city': 'Local Development',
                    'country': 'India',
                    'country_code': 'in'
                }
            elif user_ip and (user_ip.startswith('103.') or user_ip.startswith('117.') or user_ip.startswith('180.') or user_ip.startswith('14.')):
                # Common Indian IP ranges
                country = 'india'
            else:
                # Force location detection
                chatbot.get_user_location_from_ip(user_ip)
                country = chatbot.user_country or 'india'  # Default to India if detection fails
        
        # Get location-specific emergency numbers
        emergency_numbers = chatbot.get_emergency_info_by_country(country)
        
        # Determine location info
        location_info = "Unknown location"
        if chatbot.user_location:
            location_info = f"{chatbot.user_location.get('city', 'Unknown')}, {chatbot.user_location.get('country', 'Unknown')}"
        elif country:
            location_info = country.upper()
        
        # Create appropriate emergency message
        primary_number = emergency_numbers.get('emergency_services', '112')
        message = f'If you are experiencing a medical emergency, call {primary_number} immediately.'
        
        return jsonify({
            'location': location_info,
            'country_code': country,
            'detected_country': chatbot.user_country,
            'emergency_numbers': emergency_numbers,
            'emergency_symptoms': chatbot.medical_knowledge['emergency_symptoms'],
            'message': message,
            'user_ip': user_ip,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        # Fallback to India's emergency info since that's what user expects
        india_emergency = chatbot.medical_knowledge['emergency_numbers']['india']
        return jsonify({
            'location': 'India (Fallback)',
            'country_code': 'india',
            'emergency_numbers': india_emergency,
            'emergency_symptoms': chatbot.medical_knowledge['emergency_symptoms'],
            'message': f'If you are experiencing a medical emergency, call {india_emergency["emergency_services"]} immediately.',
            'error': str(e),
            'fallback': True
        })

@app.route('/api/remedies/<symptom>', methods=['GET'])
def get_remedies(symptom):
    try:
        symptom_lower = symptom.lower()
        if symptom_lower in chatbot.medical_knowledge['symptoms']:
            symptom_info = chatbot.medical_knowledge['symptoms'][symptom_lower]
            return jsonify({
                'symptom': symptom,
                'home_remedies': symptom_info.get('home_remedies', []),
                'medicines': symptom_info.get('medicines', []),
                'advice': symptom_info.get('advice', ''),
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({'error': f'No remedies found for {symptom}'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/medicines/<symptom>', methods=['GET'])
def get_medicines(symptom):
    try:
        symptom_lower = symptom.lower()
        if symptom_lower in chatbot.medical_knowledge['symptoms']:
            symptom_info = chatbot.medical_knowledge['symptoms'][symptom_lower]
            medicines = symptom_info.get('medicines', [])
            return jsonify({
                'symptom': symptom,
                'medicines': medicines,
                'disclaimer': 'Please consult with a healthcare professional before taking any medication. Always read labels and follow dosage instructions.',
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({'error': f'No medicines found for {symptom}'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/medicine-search/<medicine_name>', methods=['GET'])
def medicine_search(medicine_name):
    try:
        search_results = chatbot.search_medicine_online(medicine_name)
        return jsonify({
            'medicine_name': medicine_name,
            'pharmacy_links': search_results,
            'message': f'Search results for {medicine_name} across multiple pharmacies',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/location', methods=['GET'])
def get_location():
    try:
        user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        location = chatbot.get_user_location_from_ip(user_ip)
        return jsonify({
            'location': location,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/hospitals-nearby', methods=['POST'])
def hospitals_nearby():
    try:
        data = request.get_json()
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        radius = data.get('radius', 5000)
        
        if not latitude or not longitude:
            # Try to use stored location
            if chatbot.user_location:
                latitude = chatbot.user_location.get('latitude')
                longitude = chatbot.user_location.get('longitude')
        
        if not latitude or not longitude:
            return jsonify({'error': 'Location coordinates required'}), 400
        
        hospital_info = chatbot.find_nearby_hospitals(latitude, longitude, radius)
        
        # Get location-specific emergency numbers
        emergency_numbers = chatbot.get_emergency_info_by_country()
        
        return jsonify({
            'hospital_search': hospital_info,
            'location_used': {'latitude': latitude, 'longitude': longitude},
            'emergency_numbers': emergency_numbers,
            'location_info': chatbot.user_location,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/traditional-remedies/<symptom>', methods=['GET'])
def get_traditional_remedies_api(symptom):
    try:
        country = request.args.get('country', chatbot.user_country)
        remedies = chatbot.get_traditional_remedies(symptom, country)
        
        return jsonify({
            'symptom': symptom,
            'country': country,
            'traditional_remedies': remedies,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/emergency-info/<country>', methods=['GET'])
def get_country_emergency_info(country):
    try:
        emergency_numbers = chatbot.get_emergency_info_by_country(country.lower())
        
        return jsonify({
            'country': country,
            'emergency_numbers': emergency_numbers,
            'emergency_symptoms': chatbot.medical_knowledge['emergency_symptoms'],
            'message': f'Emergency information for {country.upper()}',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/set-location/<country>', methods=['POST'])
def set_user_location(country):
    try:
        chatbot.user_country = country.lower()
        chatbot.user_location = {
            'city': 'User Set',
            'country': country.title(),
            'country_code': country.lower()
        }
        
        return jsonify({
            'success': True,
            'message': f'Location set to {country.title()}',
            'user_location': chatbot.user_location,
            'user_country': chatbot.user_country,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 