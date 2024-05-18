import re
import csv
import argparse

class Threat:
    def __init__(self, summary="", threat_number=0, priority="", category="", description="", sdl_phase="", mitigations=""):
        self.summary = summary
        self.threat_number = threat_number
        self.priority = priority
        self.category = category
        self.description = description
        self.sdl_phase = sdl_phase
        self.mitigations = mitigations
    
    def __str__(self):
        return f'{self.summary},{self.threat_number},{self.priority},{self.category},{self.description},{self.sdl_phase},{self.mitigations}'

class Interaction:
    def __init__(self, name="default_interaction", threats=None):
        if threats is None:
            threats = []
        self.name = name
        self.threats = threats
    
    def SetName(self, name):
        self.name = name
    
    def AddThreat(self, threat):
        self.threats.append(threat)

def set_threat_attribute(line, threat):
    pattern = r'(\d+)\.\s+(.*?)\s+\[Priority:\s(.*?)\]'

    match = re.match(pattern, line)
    if match:
        threat.threat_number = int(match.group(1))
        threat.summary = match.group(2)
        threat.priority = match.group(3)

    attributes_mapping = {
        "Category:": "category",
        "Description:": "description",
        "SDL Phase:": "sdl_phase",
        "Possible Mitigation(s):": "mitigations"
    }
    
    for key, value in attributes_mapping.items():
        if key in line:
            setattr(threat, value, line.split(key)[1].strip())
            return threat
    
    return threat

def check_all_fields_set(threat):
    for k, v in vars(threat).items():
        if v == "" or v == 0:
            return False
    return True

def serialize_to_csv(interactions, filename='output.csv'):
    # Define the CSV headers
    headers = [
        'Interaction Name', 'Threat Number', 'Summary', 'Priority', 
        'Category', 'Description', 'SDL Phase', 'Mitigations'
    ]
    
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(headers)
        
        # Write the data rows
        for interaction in interactions:
            for threat in interaction.threats:
                writer.writerow([
                    interaction.name, threat.threat_number, threat.summary, 
                    threat.priority, threat.category, threat.description, 
                    threat.sdl_phase, threat.mitigations
                ])

def main():

    parser = argparse.ArgumentParser(description="CSV serializer for MTMT threat analysis")
    parser.add_argument("--input-file",type=str,help="Path for file to be parsed (an initially parsed threats file - use ./initial_mtmt_scrape.sh to get valid results)")
    parser.add_argument("--output-path",type=str,help="Path for serialized output (directory name)")

    args = parser.parse_args()

    INPUT_FILE =args.input_file
    DIRECTORY = args.output_path
    if args.output_path == "":
        DIRECTORY="."
    if args.input_file == "":
        print("Error: no input file")
        exit


    with open(INPUT_FILE, 'r') as file:
        lines = file.readlines()

    interactions = []
    current_interaction = None
    current_threat = None

    for line in lines:
        line = line.strip()
        if line.startswith("Interaction:"):
            if current_interaction:
                if current_threat and check_all_fields_set(current_threat):
                    current_interaction.AddThreat(current_threat)
                interactions.append(current_interaction)
            interaction_name = line.split(":")[1].strip()
            current_interaction = Interaction(name=interaction_name)
            current_threat = None
        elif re.match(r'\d+\.\s+', line):
            if current_threat and check_all_fields_set(current_threat):
                current_interaction.AddThreat(current_threat)
            current_threat = set_threat_attribute(line, Threat())
        else:
            if current_threat:
                current_threat = set_threat_attribute(line, current_threat)

    # Add the last threat and interaction if necessary
    if current_interaction:
        if current_threat and check_all_fields_set(current_threat):
            current_interaction.AddThreat(current_threat)
        interactions.append(current_interaction)

    serialize_to_csv(interactions,f'{DIRECTORY}/data.csv')

if __name__ == "__main__":
    main()
