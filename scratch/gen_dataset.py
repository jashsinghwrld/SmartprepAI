import json
import random

# ─── CBSE Class-wise Curriculum ───────────────────────────────────────────────
CBSE_CURRICULUM = {
    9: {
        "physics": {
            "Motion": ["Distance and Displacement", "Velocity and Speed", "Acceleration", "Uniform Motion", "Graphical Representation", "Equations of Motion"],
            "Force and Laws of Motion": ["Newton's First Law", "Newton's Second Law", "Newton's Third Law", "Inertia", "Momentum", "Conservation of Momentum"],
            "Gravitation": ["Universal Law of Gravitation", "Free Fall", "Mass vs Weight", "Thrust and Pressure", "Archimedes Principle", "Buoyancy"],
            "Work Energy Power": ["Work Done", "Kinetic Energy", "Potential Energy", "Conservation of Energy", "Power", "Commercial Unit of Energy"],
            "Sound": ["Wave Motion", "Frequency and Amplitude", "Speed of Sound", "Reflection of Sound", "Echo", "SONAR"],
        },
        "chemistry": {
            "Matter in Our Surroundings": ["States of Matter", "Evaporation", "Interconversion of States", "Latent Heat", "Diffusion"],
            "Is Matter Around Us Pure": ["Mixtures and Solutions", "Colloids and Suspensions", "Separation Techniques", "Elements and Compounds", "Physical and Chemical Changes"],
            "Atoms and Molecules": ["Dalton's Atomic Theory", "Atomic Mass", "Mole Concept", "Molecules of Elements", "Chemical Formulae"],
            "Structure of Atom": ["Electrons Protons Neutrons", "Bohr's Model", "Atomic Number and Mass Number", "Isotopes and Isobars", "Valence Electrons"],
            "Chemical Bonding Basics": ["Ionic Bonding", "Covalent Bonding", "Valency", "Lewis Structure"],
        },
        "maths": {
            "Number Systems": ["Irrational Numbers", "Real Numbers on Number Line", "Laws of Exponents", "Decimal Expansion", "Representation on Line"],
            "Polynomials": ["Degree of Polynomial", "Zeroes of Polynomial", "Remainder Theorem", "Factor Theorem", "Algebraic Identities"],
            "Linear Equations in Two Variables": ["Standard Form", "Graphical Solution", "Infinite Solutions", "Equation of Lines", "Word Problems"],
            "Triangles": ["Congruence of Triangles", "SAS and ASA Rules", "Isosceles Triangle Properties", "Inequalities in Triangle", "RHS Congruence"],
            "circles": ["Chord and Arc", "Angle in Semicircle", "Equal Chords", "Cyclic Quadrilateral", "Tangent Properties"],
            "Statistics": ["Mean Median Mode", "Bar Graphs", "Frequency Polygon", "Histograms", "Graphical Representation"],
            "Probability Basics": ["Experimental Probability", "Events", "Sample Space", "Likelihood of Events", "Simple Experiments"],
        },
        "biology": {
            "Cell - Basic Unit of Life": ["Cell Theory", "Prokaryotic vs Eukaryotic", "Cell Organelles", "Cell Membrane", "Nucleus and Mitochondria"],
            "Tissues": ["Meristematic Tissue", "Permanent Tissue", "Connective Tissue", "Muscular Tissue", "Nervous Tissue"],
            "Diversity in Living Organisms": ["Classification Basis", "Five Kingdom Classification", "Monera and Protista", "Plants and Animals", "Nomenclature"],
            "Why Do We Fall Ill": ["Health and Disease", "Causes of Disease", "Infectious Diseases", "Antibiotics", "Prevention and Treatment"],
            "Natural Resources": ["Air and Water Resources", "Biogeochemical Cycles", "Ozone Layer", "Soil Formation", "Rain Water Conservation"],
        }
    },
    10: {
        "physics": {
            "Light Reflection and Refraction": ["Laws of Reflection", "Spherical Mirrors", "Mirror Formula", "Refraction Laws", "Lens Formula", "Power of Lens"],
            "Human Eye and Colourful World": ["Structure of Eye", "Persistence of Vision", "Defects of Vision", "Dispersion", "Atmospheric Refraction", "Scattering of Light"],
            "Electricity": ["Electric Current", "Ohm's Law", "Resistance", "Resistors in Series and Parallel", "Heating Effect", "Electric Power"],
            "Magnetic Effects of Current": ["Magnetic Field", "Solenoid", "Fleming's Left Hand Rule", "Electric Motor", "Electromagnetic Induction", "Electric Generator"],
            "Sources of Energy": ["Fossil Fuels", "Biomass", "Wind Energy", "Solar Energy", "Nuclear Energy", "Hydropower"],
        },
        "chemistry": {
            "Chemical Reactions and Equations": ["Balancing Equations", "Types of Reactions", "Combination Reaction", "Decomposition", "Displacement Reaction", "Oxidation and Reduction"],
            "Acids Bases and Salts": ["Properties of Acids", "Properties of Bases", "pH Scale", "Neutralisation", "Common Salts", "Water of Crystallisation"],
            "Metals and Non-metals": ["Physical Properties", "Chemical Properties", "Reactivity Series", "Extraction of Metals", "Corrosion", "Alloys"],
            "Carbon and Its Compounds": ["Covalent Bonding in Carbon", "Homologous Series", "Functional Groups", "Alcohols and Carboxylic Acids", "Soaps and Detergents"],
            "Periodic Classification": ["Newlands' Law of Octaves", "Mendeleev's Table", "Modern Periodic Table", "Periodicity", "Valence Electrons"],
        },
        "maths": {
            "Real Numbers": ["Euclid's Division Lemma", "Fundamental Theorem of Arithmetic", "HCF and LCM", "Irrational Numbers Proof", "Decimal Expansion"],
            "Polynomials": ["Zeroes and Coefficients", "Division Algorithm", "Quadratic Polynomials", "Geometric Meaning of Zeroes"],
            "Quadratic Equations": ["Standard Form", "Factorisation Method", "Quadratic Formula", "Discriminant", "Nature of Roots", "Word Problems"],
            "Arithmetic Progressions": ["General Term", "Sum of n Terms", "Finding n-th Term", "AP in Daily Life", "Arithmetic Mean"],
            "Coordinate Geometry": ["Distance Formula", "Section Formula", "Midpoint Formula", "Area of Triangle", "Collinearity"],
            "Introduction to Trigonometry": ["Trigonometric Ratios", "Ratios of Specific Angles", "Trigonometric Identities", "Complementary Angles", "Applications"],
            "Surface Areas and Volumes": ["Cylinder", "Cone", "Sphere and Hemisphere", "Frustum of Cone", "Combination of Solids"],
            "Statistics": ["Mean by Direct Method", "Mode of Grouped Data", "Median of Grouped Data", "Ogives", "Cumulative Frequency"],
        },
        "biology": {
            "Life Processes": ["Nutrition", "Respiration", "Transpiration", "Blood Circulation", "Excretion"],
            "Control and Coordination": ["Nervous System", "Reflex Action", "Brain Structure", "Endocrine System", "Plant Hormones"],
            "Reproduction": ["Asexual Reproduction", "Sexual Reproduction in Plants", "Human Reproductive System", "Menstrual Cycle", "Contraception"],
            "Heredity and Evolution": ["Mendel's Laws", "Dominant and Recessive Traits", "DNA and Genes", "Speciation", "Darwin's Theory"],
            "Our Environment": ["Ecosystem", "Food Chains and Webs", "Ozone Depletion", "Waste Management", "Biodegradable Waste"],
        }
    },
    11: {
        "physics": {
            "Units and Measurement": ["SI Units", "Dimensional Analysis", "Significant Figures", "Error Analysis", "Dimensional Formulae"],
            "Motion in a Straight Line": ["Position and Velocity", "Instantaneous Speed", "Uniform Acceleration", "Kinematic Equations", "Free Fall"],
            "Motion in a Plane": ["Projectile Motion", "Circular Motion", "Relative Velocity", "Vector Addition", "Resolution of Vectors"],
            "Laws of Motion": ["Newton's Laws", "Friction", "Circular Motion Dynamics", "Banking of Roads", "Pseudo Force"],
            "Work Energy Power": ["Work-Energy Theorem", "Conservative Forces", "Potential Energy", "Elastic Collisions", "Power"],
            "Thermodynamics": ["Zeroth Law", "First Law of Thermodynamics", "Specific Heat", "Carnot Engine", "Entropy"],
            "Oscillations": ["SHM", "Spring Mass System", "Energy in SHM", "Damped Oscillations", "Forced Oscillations"],
            "Waves": ["Wave Properties", "Speed of Sound", "Superposition", "Beats", "Doppler Effect"],
        },
        "chemistry": {
            "Atomic Structure": ["Bohr's Model", "Quantum Mechanical Model", "Quantum Numbers", "Aufbau Principle", "Hund's Rule", "Electronic Configuration"],
            "Chemical Bonding": ["Ionic Bonding", "Covalent Bond", "VSEPR Theory", "Hybridization", "Molecular Orbital Theory", "Bond Parameters"],
            "States of Matter": ["Kinetic Molecular Theory", "Gas Laws", "Ideal Gas Equation", "Liquefaction", "Surface Tension"],
            "Thermodynamics": ["System and Surroundings", "Internal Energy", "Enthalpy", "Hess's Law", "Entropy and Gibbs Energy"],
            "Equilibrium": ["Law of Mass Action", "Equilibrium Constant", "Le Chatelier's Principle", "Ionic Equilibrium", "pH Calculation", "Buffer Solutions"],
            "Hydrocarbons": ["Alkanes Nomenclature", "Alkene Reactivity", "Alkynes", "Aromatic Compounds", "Markovnikov's Rule", "Benzene Structure"],
        },
        "maths": {
            "Sets": ["Types of Sets", "Set Operations", "Venn Diagrams", "De Morgan's Laws", "Cartesian Product"],
            "Relations and Functions": ["Domain and Range", "Types of Functions", "Composition", "Inverse Function", "Binary Operations"],
            "Trigonometric Functions": ["Radian Measure", "Trigonometric Identities", "Graphs of Trig Functions", "Inverse Trig", "Principal Value"],
            "Complex Numbers": ["Imaginary Unit", "Argand Plane", "Modulus and Argument", "Polar Form", "De Moivre's Theorem"],
            "Permutations and Combinations": ["Fundamental Principle", "Factorial Notation", "Permutations", "Combinations", "Pascal's Triangle"],
            "Binomial Theorem": ["Binomial Expansion", "General Term", "Middle Term", "Binomial Coefficients", "Applications"],
            "Limits and Derivatives": ["Limit Definition", "Algebra of Limits", "Standard Limits", "Derivative Definition", "Rules of Differentiation"],
            "Statistics": ["Mean Deviation", "Variance", "Standard Deviation", "Frequency Distribution", "Coefficient of Variation"],
        },
        "biology": {
            "Cell Structure and Function": ["Cell Theory", "Prokaryotic Cell", "Eukaryotic Cell", "Cell Membrane Model", "Organelles"],
            "Cell Division": ["Mitosis Phases", "Meiosis Phases", "Cell Cycle", "Significance of Meiosis", "Checkpoints"],
            "Photosynthesis": ["Light Reactions", "Dark Reactions", "Calvin Cycle", "Factors Affecting Photosynthesis", "C4 Plants"],
            "Respiration in Plants": ["Glycolysis", "Krebs Cycle", "Electron Transport Chain", "Fermentation", "Respiratory Quotient"],
            "Plant Growth": ["Growth Regions", "Auxins", "Gibberellins", "Cytokinins", "Abscisic Acid", "Seed Dormancy"],
            "Neural Control": ["Nervous System Structure", "Neuron Anatomy", "Action Potential", "Synapse", "Reflex Arc", "Brain Regions"],
            "Chemical Coordination": ["Endocrine Glands", "Hormones", "Feedback Mechanisms", "Thyroid Disorders", "Insulin and Glucagon"],
        }
    },
    12: {
        "physics": {
            "Electrostatics": ["Coulomb's Law", "Electric Field", "Gauss's Theorem", "Electric Potential", "Capacitance", "Dielectrics"],
            "Current Electricity": ["Ohm's Law", "Kirchhoff's Laws", "Wheatstone Bridge", "Potentiometer", "Resistivity", "EMF and Internal Resistance"],
            "Magnetic Effects of Current": ["Biot-Savart Law", "Ampere's Law", "Force on Current", "Moving Coil Galvanometer", "Cyclotron"],
            "Electromagnetic Induction": ["Faraday's Law", "Lenz's Law", "Motional EMF", "Eddy Currents", "Mutual Inductance", "Self Inductance"],
            "Alternating Current": ["AC Generator", "RMS Values", "LC Circuit", "Resonance", "Power Factor", "Transformer"],
            "Optics": ["Lens Maker's Formula", "Total Internal Reflection", "Microscope and Telescope", "Interference", "Diffraction", "Polarisation"],
            "Dual Nature of Matter": ["Photoelectric Effect", "Einstein's Equation", "De Broglie Wavelength", "Davisson-Germer Experiment", "Electron Emission"],
            "Atoms and Nuclei": ["Bohr Model", "Energy Levels", "Radioactivity", "Nuclear Fission and Fusion", "Binding Energy", "Half Life"],
            "Semiconductor Electronics": ["Energy Bands", "p-n Junction", "Rectifier Circuits", "Transistor Action", "Logic Gates"],
        },
        "chemistry": {
            "Solutions": ["Molarity and Molality", "Raoult's Law", "Colligative Properties", "Osmotic Pressure", "Van't Hoff Factor"],
            "Electrochemistry": ["Galvanic Cell", "EMF Calculation", "Nernst Equation", "Electrolysis", "Kohlrausch's Law", "Faraday's Laws"],
            "Chemical Kinetics": ["Rate of Reaction", "Rate Law", "Order of Reaction", "Activation Energy", "Arrhenius Equation", "Half Life"],
            "d and f Block Elements": ["Properties of Transition Metals", "Oxidation States", "Complex Formation", "Catalytic Properties", "Lanthanides"],
            "Coordination Compounds": ["Werner's Theory", "IUPAC Nomenclature", "Isomerism", "Crystal Field Theory", "Stability Constants"],
            "Haloalkanes and Haloarenes": ["IUPAC Nomenclature", "SN1 and SN2 Reactions", "Elimination Reaction", "Nucleophilicity", "Optical Isomerism"],
            "Alcohols Phenols Ethers": ["Classification", "Preparation Methods", "Chemical Properties", "Acidity Comparison", "Ether Reactions"],
            "Aldehydes Ketones Acids": ["Nucleophilic Addition", "Cannizzaro Reaction", "Aldol Condensation", "Carboxylic Acid Reactions", "Acidity"],
        },
        "maths": {
            "Relations and Functions": ["Types of Relations", "Types of Functions", "Composition", "Invertible Functions", "Binary Operations"],
            "Inverse Trigonometry": ["Domain and Range", "Principal Values", "Properties of Inverse Trig", "Identities", "Equations"],
            "Matrices": ["Types of Matrices", "Matrix Operations", "Transpose", "Symmetric Matrix", "Invertible Matrix"],
            "Determinants": ["Properties of Determinants", "Cofactors and Minors", "Adjoint", "Inverse Matrix", "Cramer's Rule"],
            "Continuity and Differentiability": ["Continuity Conditions", "Differentiability", "Chain Rule", "Implicit Differentiation", "Logarithmic Differentiation", "Rolle's Theorem"],
            "Applications of Derivatives": ["Rate of Change", "Increasing and Decreasing", "Maxima and Minima", "Tangents and Normals", "Approximations"],
            "Integrals": ["Integration by Substitution", "Integration by Parts", "Partial Fractions", "Definite Integrals", "Properties of Definite Integrals"],
            "Differential Equations": ["Order and Degree", "Variable Separable", "Homogeneous Equations", "Linear Differential Equations", "Applications"],
            "Vector Algebra": ["Types of Vectors", "Addition and Subtraction", "Dot Product", "Cross Product", "Section Formula in 3D"],
            "Probability": ["Conditional Probability", "Multiplication Theorem", "Bayes Theorem", "Bernoulli Trials", "Binomial Distribution"],
        },
        "biology": {
            "Sexual Reproduction in Plants": ["Flower Structure", "Pollination", "Double Fertilization", "Seed and Fruit Development", "Apomixis"],
            "Human Reproduction": ["Male Reproductive System", "Female Reproductive System", "Gametogenesis", "Fertilization", "Foetal Development"],
            "Reproductive Health": ["STDs", "Contraception Methods", "Infertility", "Amniocentesis", "Reproductive Technologies"],
            "Principles of Inheritance": ["Mendel's Laws", "Dominance and Recessiveness", "Dihybrid Cross", "Sex Determination", "Linkage"],
            "Molecular Basis of Inheritance": ["DNA Structure", "DNA Replication", "Transcription", "Translation", "Genetic Code", "Mutation"],
            "Evolution": ["Origin of Life", "Darwin's Natural Selection", "Evidences of Evolution", "Human Evolution", "Hardy Weinberg Principle"],
            "Human Health and Disease": ["Innate and Acquired Immunity", "Vaccines", "AIDS", "Cancer Biology", "Drug Abuse"],
            "Biotechnology": ["Recombinant DNA Technology", "PCR", "Gel Electrophoresis", "Cloning", "Transgenic Organisms"],
            "Ecosystem": ["Food Chains and Webs", "Energy Flow", "Nutrient Cycling", "Ecological Pyramids", "Succession"],
        }
    }
}

DIFFICULTIES = ["easy", "medium", "hard"]

dataset = []

for cls, subjects in CBSE_CURRICULUM.items():
    for subject, chapters in subjects.items():
        for chapter, topics in chapters.items():
            # Generate 15-25 questions per chapter
            count = random.randint(15, 25)
            for i in range(count):
                topic = random.choice(topics)
                
                # Varied difficulty distribution per chapter (gives unique profiles)
                r = random.random()
                weights = [random.uniform(0.1, 0.9) for _ in range(3)]
                total_w = sum(weights)
                weights = [w / total_w for w in weights]
                
                if r < weights[0]:
                    diff = "easy"
                elif r < weights[0] + weights[1]:
                    diff = "medium"
                else:
                    diff = "hard"
                
                dataset.append({
                    "year": random.randint(2015, 2024),
                    "class": cls,
                    "subject": subject,
                    "chapter": chapter,
                    "topic": topic,
                    "difficulty": diff,
                    "question": f"[Class {cls} {subject.capitalize()}] Explain the concept of {topic} as it applies to {chapter}.",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "answer": "Option A",
                    "explanation": f"This tests understanding of {topic} from the {chapter} chapter in Class {cls} {subject.capitalize()} (CBSE)."
                })

random.shuffle(dataset)
print(f"Generated {len(dataset)} CBSE-aligned questions across all classes and subjects.")

# Verify class coverage
from collections import Counter
class_counts = Counter(str(d['class']) + '-' + d['subject'] for d in dataset)
for k in sorted(class_counts):
    print(f"  {k}: {class_counts[k]} questions")

with open('c:/Users/jashs/Desktop/SmartprepAI/SmartprepAI/dataset/pyqs.json', 'w', encoding='utf-8') as f:
    json.dump(dataset, f, indent=2, ensure_ascii=False)

print("Dataset written to pyqs.json")
