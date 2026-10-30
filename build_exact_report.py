import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def generate_report():
    doc = Document()

    # Standard Page Setup: 1-inch margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Style definitions
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Times New Roman'
    style_normal.font.size = Pt(12)
    style_normal.font.color.rgb = RGBColor(0, 0, 0)
    style_normal.paragraph_format.line_spacing = 1.15
    style_normal.paragraph_format.space_after = Pt(6)

    def add_title(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(12)
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(16)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 0, 0)

    def add_heading_1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_heading_2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_heading_3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_p(text, bold_prefix="", italic=False):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_bold = p.add_run(bold_prefix)
            r_bold.font.bold = True
        r = p.add_run(text)
        r.font.italic = italic
        return p

    def add_bullet(text, bold_prefix=""):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_bold = p.add_run(bold_prefix)
            r_bold.font.bold = True
        p.add_run(text)
        return p

    def add_code_block(code_text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.0
        run = p.add_run(code_text)
        run.font.name = 'Courier New'
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(30, 30, 30)
        return p

    def format_table_headers(table, headers, col_widths=None):
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        hdr_row = table.rows[0]
        for idx, header_text in enumerate(headers):
            cell = hdr_row.cells[idx]
            set_cell_background(cell, "2E4053")
            set_cell_margins(cell, top=120, bottom=120, left=140, right=140)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_after = Pt(0)
            run = p.add_run(header_text)
            run.font.name = 'Times New Roman'
            run.font.bold = True
            run.font.size = Pt(10)
            run.font.color.rgb = RGBColor(255, 255, 255)
            if col_widths and idx < len(col_widths):
                cell.width = Inches(col_widths[idx])

    def add_table_row(table, row_data, is_even=False, col_widths=None):
        row = table.add_row()
        for idx, text in enumerate(row_data):
            cell = row.cells[idx]
            if is_even:
                set_cell_background(cell, "F2F4F4")
            set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.15
            run = p.add_run(str(text))
            run.font.name = 'Times New Roman'
            run.font.size = Pt(9.5)
            run.font.color.rgb = RGBColor(0, 0, 0)
            if col_widths and idx < len(col_widths):
                cell.width = Inches(col_widths[idx])

    # =========================================================================
    # COVER PAGE
    # =========================================================================
    add_title("INDUSTRIAL TRAINING REPORT ON MACHINE LEARNING PROJECT:\nSMARTPHONE FAIR PRICE PREDICTION AND VALUATION SYSTEM (WORTHIT)")
    
    add_p("Submitted in partial fulfillment of the requirements for the award of the Diploma in Computer Engineering / Information Technology under Maharashtra State Board of Technical Education (MSBTE), Mumbai.")
    
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(12)
    p_sub.paragraph_format.space_after = Pt(12)
    p_sub.add_run("Submitted By:\n").font.bold = True
    p_sub.add_run("Name: [YOUR FULL NAME]\nEnrollment Number: [YOUR ENROLLMENT NUMBER]\nAcademic Year: 2026-2027\n")
    p_sub.add_run("Department: Department of Computer Engineering / Information Technology\n")
    p_sub.add_run("Institute Name: [YOUR COLLEGE NAME]\n")
    p_sub.add_run("Training Organization: InfoStack Software Development, Training and Research Center, Solapur\n")

    doc.add_page_break()

    # =========================================================================
    # ABSTRACT
    # =========================================================================
    add_heading_1("ABSTRACT")
    add_p("Industrial training is a pivotal component of the Maharashtra State Board of Technical Education (MSBTE) curriculum, designed to bridge the gap between theoretical classroom learning and real-world industrial software engineering practices. This report details a six-week intensive industrial training program undertaken at InfoStack Software Development, Training and Research Center, Solapur.")
    add_p("During this period, focus was placed on applied data analytics, machine learning engineering, and intelligent web application development using Python, NumPy, Pandas, Matplotlib, Scikit-Learn, XGBoost, Flask, and SQLite. To ensure a thorough understanding of foundational machine learning pipelines, data preprocessing, gradient boosting mechanics, regression metrics, and responsive full-stack interfaces, the project was developed from first principles with an end-to-end data-to-deployment architecture.")
    add_p("The primary project completed during the training was a feature-rich, intelligent Web-Based Smartphone Fair Price Prediction and Valuation System entitled 'WorthIt'. The application features automated data cleaning and dynamic variant mapping across 2,983 smartphone configurations, high-accuracy price estimation using an optimized XGBoost Regressor (achieving R2 = 0.93+), a dynamic heuristic confidence scoring engine bounded between 65% and 96%, an intelligent multi-criteria 'Smarter Alternatives' recommender engine with penalty ranking and distinct top-match visual styling, SQLite user data persistence, and a modern responsive user interface built with HTML5, CSS3, JavaScript, and Jinja2 templating. This report covers the software development lifecycle (SDLC), machine learning pipelines, schema design, comprehensive test cases, workplace safety, technical challenges, and core learning outcomes experienced at InfoStack Solapur.")

    doc.add_page_break()

    # =========================================================================
    # ACKNOWLEDGEMENT
    # =========================================================================
    add_heading_1("ACKNOWLEDGEMENT")
    add_p("I express my deepest gratitude to InfoStack Software Development, Training and Research Center, Solapur for granting me the opportunity to undergo six weeks of practical industrial training at their technical facility.")
    add_p("I express my sincere appreciation to the Managing Director and Industry Mentors at InfoStack Solapur, whose guidance, technical insights, and continuous encouragement provided an invaluable environment for learning real-world data science, machine learning pipelines, and full-stack software development practices.")
    add_p("I am profoundly grateful to our Principal, [PRINCIPAL NAME], and Head of Department, [HOD NAME], for their encouragement and administrative support throughout the industrial training program.")
    add_p("Special thanks are extended to my Internal Guide, [YOUR GUIDE / MENTOR NAME], for continuous evaluation, constructive feedback, and oversight during the documentation of this report. Finally, I thank my family and fellow peers for their unwavering support and motivation.")
    
    p_ack_sign = doc.add_paragraph()
    p_ack_sign.paragraph_format.space_before = Pt(14)
    p_ack_sign.add_run("[YOUR FULL NAME]\n").font.bold = True
    p_ack_sign.add_run("Enrollment No: [YOUR ENROLLMENT NUMBER]")

    doc.add_page_break()

    # =========================================================================
    # TABLE OF CONTENTS
    # =========================================================================
    add_heading_1("TABLE OF CONTENTS")
    
    toc_table = doc.add_table(rows=1, cols=3)
    format_table_headers(toc_table, ["Sr. No", "Chapter", "Page No"], [0.8, 4.7, 1.0])
    
    toc_data = [
        ["1", "Organization Structure of Industry and General Layout", "1"],
        ["2", "Introduction to Industry / Organization", "4"],
        ["3", "Types of Major Equipments / Hardware / Software Used in Industry", "7"],
        ["4", "Processes and Software Development Methodology", "11"],
        ["5", "Testing of Hardware and Software", "14"],
        ["6", "Safety Procedures and Work Environment Practices", "18"],
        ["7", "Particulars of Practical Experiences in Industry", "19"],
        ["8", "Detailed Report of the Tasks Undertaken (WorthIt Smartphone Valuation Project)", "21"],
        ["9", "Special / Challenging Experiences Encountered During Training", "26"],
        ["10", "Conclusion", "27"],
        ["11", "References / Sources of Information", "29"],
    ]
    for idx, row in enumerate(toc_data):
        add_table_row(toc_table, row, is_even=(idx % 2 == 1), col_widths=[0.8, 4.7, 1.0])

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 1
    # =========================================================================
    add_heading_1("CHAPTER 1: ORGANIZATION STRUCTURE OF INDUSTRY AND GENERAL LAYOUT")
    add_heading_2("1.1 Organizational Structure of InfoStack Solapur")
    add_p("InfoStack Software Development, Training and Research Center operates under a structured organizational framework to ensure seamless software delivery, robust technical research, and quality industrial training.")
    add_p("Key Administrative and Technical Roles:", bold_prefix="")
    add_bullet("Managing Director (MD): Oversees strategic growth, client acquisition, and overall corporate vision.")
    add_bullet("Technical Director & Project Managers: Drive project planning, resource allocation, technical architecture validation, and client requirement sign-offs.")
    add_bullet("Senior Software Engineers & ML Leads: Responsible for machine learning pipeline design, enterprise database modeling, predictive model tuning, and technical guidance.")
    add_bullet("Quality Assurance (QA) Engineers: Conduct automated and manual testing, performance verification, cross-browser validation, and prediction consistency audits.")
    add_bullet("Systems & Infrastructure Administrators: Maintain local deployment servers, developer workstations, high-availability networks, and secure repository backups.")
    add_bullet("Research & Industrial Training Division: Directs technical internship programs, conducts applied AI research, and bridges academic curricula with industry practices.")

    add_heading_2("1.2 Infrastructure Layout and General Facility Distribution")
    add_p("The facility at InfoStack Solapur spans dedicated functional zones designed to maintain high productivity, data security, and collaborative learning:")
    add_bullet("Software Development Labs: High-performance development bays equipped with multi-monitor workstations, high-speed Gigabit LAN, and dedicated Python virtual environments.")
    add_bullet("Research Workstations: Dedicated setups running Linux/Windows server environments for experimental machine learning prototyping, XGBoost hyperparameter tuning, and dataset benchmarking.")
    add_bullet("Server Room & Data Hub: Climate-controlled room housing local staging servers, SQLite/MySQL database environments, firewall gateways, and network-attached storage (NAS) units for automated backups.")
    add_bullet("Training and Seminar Hall: Modern presentation setup with audiovisual systems, digital whiteboards, and high-density networking to support hands-on industrial training sessions.")
    add_bullet("Administrative and Conference Rooms: Dedicated spaces for sprint planning sessions, daily stand-ups, code reviews, and project evaluations.")

    # =========================================================================
    # CHAPTER 2
    # =========================================================================
    add_heading_1("CHAPTER 2: INTRODUCTION TO INDUSTRY / ORGANIZATION")
    add_heading_2("2.1 History and Background")
    add_p("InfoStack Software Development, Training and Research Center, Solapur, stands as a prominent software firm and technology research facility in the Solapur region of Maharashtra. Established to deliver software engineering solutions to regional, national, and enterprise clients, InfoStack has built a reputation for high-performance software architecture, enterprise web platforms, custom AI/ML analytics, and industrial talent development.")
    add_p("Recognizing the technical skill gaps faced by diploma and degree engineering graduates, InfoStack established its dedicated Research and Industrial Training wing. This wing operates as a live production environment where interns work on real-world projects, modern design patterns, strict coding conventions, and software engineering protocols.")

    add_heading_2("2.2 Core Products, Services, and Technical Portfolio")
    add_bullet("Applied Machine Learning & Predictive Analytics: Supervised learning models, valuation algorithms, automated recommender engines, and regression pipelines.")
    add_bullet("Full-Stack Web Application Solutions: Scalable, secure, and responsive web platforms built using Flask, Python, JavaScript, and relational database architectures.")
    add_bullet("Database Architecture and Optimization: SQLite/MySQL database schema design, indexing, parameterized query optimization, and structured persistence.")
    add_bullet("Corporate and Industrial Training: Standardized technical training programs focused on Python Programming, Data Science, Machine Learning, and Web Engineering.")

    add_heading_2("2.3 Workforce, Domain Expertise, and Industry Standing")
    add_p("InfoStack Solapur maintains a skilled team of software architects, full-stack engineers, data scientists, UI/UX designers, and QA personnel. The center focuses on native, robust software engineering, ensuring developers gain a deep understanding of data structures, statistical modeling, algorithmic complexity, and asynchronous browser interactions.")

    # =========================================================================
    # CHAPTER 3
    # =========================================================================
    add_heading_1("CHAPTER 3: TYPES OF MAJOR EQUIPMENTS / HARDWARE / SOFTWARE USED IN INDUSTRY")
    add_heading_2("3.1 Hardware Specifications and Development Workstations")
    
    hw_table = doc.add_table(rows=1, cols=3)
    format_table_headers(hw_table, ["Hardware Equipment", "Technical Configuration / Specifications", "Purpose / Function in Industry"], [1.5, 2.5, 2.5])
    hw_data = [
        ["Development Workstations", "Intel Core i5/i7 (11th/12th Gen), 16GB-32GB DDR4 RAM, 512GB NVMe SSD, Dual FHD Displays", "Primary machine for Python script execution, model training, and web development."],
        ["Local Staging Servers", "Dell PowerEdge Rack Server, Multi-core Xeon, 64GB ECC RAM, RAID 10 Storage", "Staging environment hosting Flask web services and model artifact staging."],
        ["Networking Infrastructure", "Cisco Managed Gigabit Switches, Hardware Firewall (SonicWall), Dual-band Wi-Fi Routers", "Securing network traffic, providing high-speed repository access and environment isolation."],
        ["Power Backup Systems", "15 KVA Online Uninterruptible Power Supply (UPS) with Auto-Synchronizing Generator", "Assuring continuous power to servers and workstations during grid outages."]
    ]
    for idx, row in enumerate(hw_data):
        add_table_row(hw_table, row, is_even=(idx % 2 == 1), col_widths=[1.5, 2.5, 2.5])

    add_heading_2("3.2 Software Stack, Development Tools, and Environments")
    
    sw_table = doc.add_table(rows=1, cols=4)
    format_table_headers(sw_table, ["Category", "Tool / Technology Name", "Version / Specification", "Usage / Context"], [1.2, 1.8, 1.5, 2.0])
    sw_data = [
        ["Operating System", "Microsoft Windows 11 Pro / Ubuntu Linux 22.04 LTS", "64-bit Systems", "Standardized OS environment for hosting Python runtimes and IDEs."],
        ["IDE / Text Editor", "Visual Studio Code / PyCharm Professional", "Latest Stable Builds", "Integrated development environment for Python, JavaScript, and HTML5."],
        ["Programming Language", "Python", "Version 3.10.x / 3.11.x", "Core backend language for data pipelines, ML modeling, and REST APIs."],
        ["ML & Analytics Libraries", "NumPy, Pandas, Matplotlib, Scikit-Learn, XGBoost, Joblib", "Latest LTS", "Data manipulation, visualization, regression modeling, and artifact serialization."],
        ["Web Framework", "Flask", "Version 2.3.x / 3.0.x", "Micro-web framework handling routing, Jinja2 templates, and RESTful endpoints."],
        ["Database System", "SQLite3", "Version 3.40+", "Embedded relational database engine for user-saved valuations and app settings."],
        ["Frontend Technologies", "HTML5, CSS3 (Modern Flexbox/Grid), Vanilla JavaScript (ES6+)", "Native Web Standards", "Interactive browser UI, dynamic dropdown cascades, and asynchronous AJAX."],
        ["Version Control", "Git & GitHub", "Command-Line & Web UI", "Version control, feature branching, and collaborative code management."]
    ]
    for idx, row in enumerate(sw_data):
        add_table_row(sw_table, row, is_even=(idx % 2 == 1), col_widths=[1.2, 1.8, 1.5, 2.0])

    add_heading_2("3.3 Maintenance Protocols and Licensing Management")
    add_bullet("Licensing: Utilization of open-source technologies under permissive licenses (MIT, BSD-3, Apache 2.0) with corporate compliance standards.")
    add_bullet("Preventive Maintenance: Weekly virtual environment cleanup, package vulnerability audits via pip-audit, and SSD disk health monitoring.")
    add_bullet("Data Security: Daily automated backups of dataset repositories, trained model weights, and SQLite database snapshots.")

    # =========================================================================
    # CHAPTER 4
    # =========================================================================
    add_heading_1("CHAPTER 4: PROCESSES AND SOFTWARE DEVELOPMENT METHODOLOGY")
    add_heading_2("4.1 Software Development Life Cycle (SDLC) Model")
    add_p("InfoStack Solapur follows an Agile / Iterative SDLC Model tailored for data-driven machine learning web applications. The workflow balances statistical model iteration with robust full-stack software delivery across 5 disciplined phases:")
    add_bullet("Phase 1 - Requirements & Dataset Curation: Gathering smartphone technical specifications, defining price valuation criteria, and cleaning raw tabular records.")
    add_bullet("Phase 2 - Pipeline & System Design: Formulating preprocessing pipelines, label encoding mappings, database schemas, and wireframing user interfaces.")
    add_bullet("Phase 3 - Iterative Sprint Development: Sprint 1 (Data cleaning & dynamic maps) -> Sprint 2 (XGBoost model training & serialization) -> Sprint 3 (Recommender & confidence algorithms) -> Sprint 4 (Flask REST API & frontend integration).")
    add_bullet("Phase 4 - Quality Assurance & Validation: Validating regression metrics (R2, MAE), testing dynamic UI dropdown cascades, and executing manual test cases.")
    add_bullet("Phase 5 - Deployment & Monitoring: Local staging deployment on Flask development server, SQLite connection optimization, and documentation.")

    add_heading_2("4.2 Requirement Gathering and Systems Architecture")
    add_p("Detailed functional requirements were defined to deliver an instantaneous, transparent valuation experience:")
    add_bullet("Smart Specification Cascading: Selecting a Brand instantly filters available Models; selecting a Model dynamically filters only valid RAM, Storage, Processor, Display Type, and Network configurations.")
    add_bullet("Accurate Valuation: Calculating the Predicted Fair Price using machine learning and determining whether the phone is an 'Excellent Deal', 'Worth Buying', 'Fair Price', 'Slightly Overpriced', or 'Highly Overpriced'.")
    add_bullet("Intelligent Alternative Matching: Recommending superior or equal spec phones priced strictly between the predicted fair price and current listing price, ranking by a weighted multi-criteria penalty score, and highlighting top matches.")

    add_heading_2("4.3 Coding Standards, Version Control, and Code Reviews")
    add_bullet("PEP 8 Compliance: Strict adherence to Python style guidelines, explicit function docstrings, modular folder structuring, and descriptive variable naming.")
    add_bullet("Branching Model: Development isolated across Git branches (main, feature/dataset-clean, feature/xgboost-model, feature/recommender-logic, feature/ui-cards).")
    add_bullet("Code Review Protocols: Mandatory mentor review of data leakage risks, matrix shapes, and exception safety before merging.")

    # =========================================================================
    # CHAPTER 5
    # =========================================================================
    add_heading_1("CHAPTER 5: TESTING OF HARDWARE AND SOFTWARE")
    add_heading_2("5.1 Quality Assurance (QA) Workflows")
    add_p("Quality Assurance at InfoStack Solapur spans all development phases. The testing cycle validates machine learning inference accuracy, dynamic frontend autofill state management, API latency, and database persistence integrity.")
    add_bullet("Unit Testing: Validating individual mathematical routines such as the dynamic confidence formula, penalty score calculations, and label encoding transforms.")
    add_bullet("Integration Testing: Ensuring seamless end-to-end data flow from user form inputs -> JSON AJAX payloads -> Flask /predict controller -> Preprocessing & XGBoost inference -> Recommender engine -> JSON response -> Dynamic DOM card rendering.")
    add_bullet("UI and Cross-Browser Compatibility: Testing responsive layout behavior across Chrome, Firefox, and Edge across desktop and mobile viewports.")
    add_bullet("Database CRUD Validation: Testing SQLite parameterized insert, select, and delete queries for saved smartphone valuations and user settings.")

    add_heading_2("5.2 Manual Test Cases (Sample Execution Table)")
    
    test_table = doc.add_table(rows=1, cols=6)
    format_table_headers(test_table, ["Test Case ID", "Feature / Module", "Test Objective", "Input Data", "Expected Result", "Status"], [0.8, 1.1, 1.4, 1.2, 1.5, 0.5])
    
    test_cases_data = [
        ["TC_DP_01", "Dynamic Dropdown", "Verify Brand selection updates Model dropdown", "Select Brand = 'Apple'", "Model dropdown populates with only Apple models (e.g., iPhone 11, 12, 13, 14)", "PASS"],
        ["TC_DP_02", "Dynamic Dropdown", "Verify Model selection populates exact valid RAM/Storage variants", "Select Model = 'iPhone 11'", "RAM shows 4GB; Storage shows [64GB, 128GB, 256GB]; Processor/Display/Network auto-fill", "PASS"],
        ["TC_ML_01", "ML Prediction", "Verify fair price estimation and deal recommendation", "Apple iPhone 11 (4GB/128GB), Current Price = 39,999", "Predicted Fair Price approx Rs. 32,339; Status = 'Slightly Overpriced' (+23.7%)", "PASS"],
        ["TC_CF_01", "Confidence Scorer", "Verify dynamic confidence formula calculation", "Brand='Apple', RAM=4, Storage=128, Processor='A13 Bionic'", "Calculates confidence score between 65% and 96% (e.g., 91%) based on dataset row density", "PASS"],
        ["TC_RC_01", "Recommender", "Verify alternatives fall in price range and match specs", "Current=39,999, Predicted=32,339, RAM=4GB, Storage=128GB", "Returns alternative phones priced between Rs. 32,339 and Rs. 39,999 with RAM>=4GB, Storage>=64GB", "PASS"],
        ["TC_RC_02", "Recommender UI", "Verify top 1-3 alternatives receive 'Best Match' visual highlight", "Alternatives list returned with penalty scores", "Top 1-3 cards render with distinct terracotta/gold accent border and 'Best Match' badge", "PASS"],
        ["TC_DB_01", "Saved Phones", "Verify saving valuation record to SQLite database", "Click 'Save Valuation' button on prediction card", "AJAX POST /saved inserts record into saved_phones table; returns status 'success'", "PASS"],
        ["TC_DB_02", "Saved Phones", "Verify deletion of saved valuation record", "Click 'Delete' icon on saved phone item (ID=1)", "AJAX DELETE /saved/1 removes row from SQLite; UI removes card smoothly", "PASS"],
        ["TC_ST_01", "Settings Module", "Verify persistence of user configuration settings", "POST /settings with theme='dark', currency='INR'", "SQLite settings table updates key-value pairs; reflected upon page reload", "PASS"]
    ]
    for idx, row in enumerate(test_cases_data):
        add_table_row(test_table, row, is_even=(idx % 2 == 1), col_widths=[0.8, 1.1, 1.4, 1.2, 1.5, 0.5])

    # =========================================================================
    # CHAPTER 6
    # =========================================================================
    add_heading_1("CHAPTER 6: SAFETY PROCEDURES AND WORK ENVIRONMENT PRACTICES")
    add_heading_2("6.1 Physical, Electrical, and Ergonomic Workplace Safety")
    add_bullet("Ergonomics: Workstations configured with adjustable displays, lumbar-support seating, and neutral wrist alignment to prevent repetitive strain injuries.")
    add_bullet("Electrical Protocols: Concealed conduit wiring, surge protectors, and circuit breakers deployed across development bays.")
    add_bullet("Fire Safety: CO2 and dry-chemical fire extinguishers deployed with marked emergency exit routes.")

    add_heading_2("6.2 Data Security, Cybersecurity, and Data Privacy Practices")
    add_bullet("Role-Based Access Control: Repository write permissions and database modifications restricted to authorized team members.")
    add_bullet("Secure Query Execution: Utilization of parameterized SQL statements preventing SQL injection attacks in SQLite.")
    add_bullet("Repository Protection: Exclusion of virtual environments, cache files, and sensitive credentials via comprehensive .gitignore rules.")

    # =========================================================================
    # CHAPTER 7
    # =========================================================================
    add_heading_1("CHAPTER 7: PARTICULARS OF PRACTICAL EXPERIENCES IN INDUSTRY")
    add_heading_2("7.1 Key Technical Competencies Developed")
    add_p("During the six-week industrial training, hands-on competencies were established across modern data science, machine learning, and web development:")
    add_bullet("Data Cleansing and Preprocessing: Manipulating tabular CSV files using Pandas, cleaning missing values, stripping unit strings, and extracting dynamic relational maps for UI dropdowns.")
    add_bullet("Machine Learning Engineering: Training and evaluating Gradient Boosted Decision Trees (XGBoost Regressor), tuning tree depth and learning rates, and computing evaluation metrics (R2 Score, MAE).")
    add_bullet("Model Serialization & Deployment: Packaging trained model estimators and LabelEncoder dictionaries into pickle/joblib artifacts for instant inference.")
    add_bullet("Algorithmic Recommender Systems: Formulating multi-parameter penalty distance functions combining price deviations and memory trade-offs.")
    add_bullet("Full-Stack Web Engineering: Building Flask RESTful micro-services, structuring Jinja2 HTML templates, implementing modern CSS Grid/Flexbox layouts, and writing vanilla JavaScript for asynchronous DOM manipulation.")
    add_bullet("Relational Data Persistence: Designing SQLite schemas, executing parameterized CRUD queries, and managing local application configurations.")

    # =========================================================================
    # CHAPTER 8 (CORE TECHNICAL CHAPTER - DETAILED PROJECT REPORT)
    # =========================================================================
    add_heading_1("CHAPTER 8: DETAILED REPORT OF THE TASKS UNDERTAKEN (WORTHIT: SMARTPHONE VALUATION SYSTEM)")
    
    add_heading_2("8.1 Project Objective and Architectural Overview")
    add_p("The central project developed during the training program was an intelligent, full-stack Machine Learning Web Application entitled 'WorthIt' (Smartphone Fair Price Prediction and Valuation System). The primary objective was to eliminate consumer uncertainty in the smartphone marketplace by predicting the mathematically fair market price of any smartphone configuration, evaluating deal quality, and recommending superior value alternatives.")
    add_p("The system architecture follows a clean 4-tier decoupled pipeline:")
    add_bullet("Tier 1: Client/Browser Layer - Built using semantic HTML5, modern CSS3 (Flexbox/Grid, Glassmorphic aesthetics), and Vanilla JavaScript (ES6+). Handles dynamic multi-level dropdown cascading and asynchronous JSON communication.")
    add_bullet("Tier 2: Application Controller (Flask) - Python web service managing HTTP routing (`/`, `/prediction`, `/predict`, `/saved`, `/settings`), request validation, and JSON API responses.")
    add_bullet("Tier 3: Machine Learning & Recommender Engine - XGBoost Regressor for price inference, dynamic heuristic confidence scorer, and penalty-ranked multi-criteria alternative matching engine.")
    add_bullet("Tier 4: Relational Persistence (SQLite) - `worthit.db` managing saved valuation histories and user settings via parameterized SQL operations.")

    add_heading_2("8.2 Database Schema Design")
    add_p("The application utilizes an embedded SQLite relational database (`worthit.db`) designed for lightweight, high-speed data persistence for saved smartphone valuations and user configurations.")
    
    add_heading_3("Table Definitions and Relational Structure:")
    add_p("1. saved_phones Table", bold_prefix="")
    add_p("Stores user-bookmarked smartphone valuations, predicted prices, and calculated savings.")
    add_bullet("id: INTEGER PRIMARY KEY AUTOINCREMENT")
    add_bullet("brand: TEXT NOT NULL (Manufacturer brand name, e.g., 'Apple', 'Samsung')")
    add_bullet("model: TEXT NOT NULL (Smartphone model name, e.g., 'iPhone 11', 'Galaxy S21')")
    add_bullet("processor: TEXT (Processor / SoC name, e.g., 'A13 Bionic', 'Snapdragon 888')")
    add_bullet("ram: INTEGER NOT NULL (RAM capacity in Gigabytes)")
    add_bullet("storage: INTEGER NOT NULL (Internal storage capacity in Gigabytes)")
    add_bullet("predicted_price: REAL NOT NULL (ML predicted fair market value in INR)")
    add_bullet("current_price: REAL NOT NULL (User entered market listing price in INR)")
    add_bullet("savings: REAL (Calculated difference between listing and fair price)")
    add_bullet("timestamp: DATETIME DEFAULT CURRENT_TIMESTAMP")

    add_p("2. settings Table", bold_prefix="")
    add_p("Stores key-value pairs for customizable user preferences and system configuration.")
    add_bullet("key: TEXT PRIMARY KEY (Configuration setting key, e.g., 'theme', 'currency', 'default_brand')")
    add_bullet("value: TEXT (Associated setting value string)")

    add_heading_2("8.3 Implementation Details of Core System Modules")

    # Module 1: Preprocessing & Dynamic Maps
    add_heading_3("Module 1: Exploratory Data Analysis & Dynamic Dataset Preprocessing")
    add_p("The dataset (`smartphones.csv`) comprises 2,983 cleaned smartphone records across 27 leading brands with 11 distinct feature columns (Brand, Model, RAM, Storage, Battery Capacity, Fast Charging, Rear Camera, Processor, Display Type, Network, and Price).")
    add_p("To guarantee a zero-friction user experience, the preprocessing module extracts dynamic relationship maps so that dropdown menus on the frontend populate exclusively with valid, existing combinations:")
    add_code_block("""# utils/preprocessing.py (Dynamic Relational Map Generation)
import pandas as pd

def get_dynamic_maps():
    df = load_data('dataset/smartphones.csv')
    brands = sorted(df['Brand'].dropna().unique().tolist())
    
    full_map = {}
    for brand in brands:
        brand_df = df[df['Brand'] == brand]
        models = sorted(brand_df['Model'].dropna().unique().tolist())
        full_map[brand] = {}
        
        for model in models:
            model_df = brand_df[brand_df['Model'] == model]
            # Extract unique RAM and Storage combinations
            ram_storage_list = []
            for _, row in model_df[['RAM', 'Storage', 'Price']].drop_duplicates().iterrows():
                ram_storage_list.append({
                    'ram': int(row['RAM']),
                    'storage': int(row['Storage']),
                    'price': int(row['Price'])
                })
            
            # Extract hardware specifications
            sample_row = model_df.iloc[0]
            full_map[brand][model] = {
                'variants': ram_storage_list,
                'processor': str(sample_row.get('Processor', '')),
                'display': str(sample_row.get('Display Type', '')),
                'network': str(sample_row.get('Network', '')),
                'battery': int(sample_row.get('Battery Capacity', 0)),
                'fast_charging': int(sample_row.get('Fast Charging', 0)),
                'camera': int(sample_row.get('Rear Camera', 0))
            }
    return brands, full_map
""")

    # Module 2: XGBoost ML Training & Inference
    add_heading_3("Module 2: Machine Learning Price Prediction Engine (XGBoost Regressor)")
    add_p("The price prediction engine utilizes an optimized Extreme Gradient Boosting Regressor (`XGBRegressor`). Categorical features (Brand, Model, Processor, Display Type, Network) are encoded via Scikit-Learn's `LabelEncoder`, and the model is trained to minimize Mean Absolute Error (MAE) while maximizing the Coefficient of Determination (R2 Score).")
    add_code_block("""# model/train_model.py (XGBoost Training and Artifact Serialization)
import os, joblib
import pandas as pd
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from utils.preprocessing import load_data, preprocess_and_encode

def train():
    df = load_data('dataset/smartphones.csv')
    X = df.drop('Price', axis=1)
    y = df['Price']
    
    # Preprocess & Encode Categorical Columns
    X_processed, encoders = preprocess_and_encode(X, train=True)
    X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.2, random_state=42)
    
    # Train Gradient Boosted Decision Trees
    model = XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluation
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    print(f"Model Training Complete! MAE: Rs. {mae:.2f} | R2 Score: {r2:.4f}")
    
    # Save Model Artifacts
    os.makedirs('model', exist_ok=True)
    joblib.dump(model, 'model/model.pkl')
    joblib.dump(encoders, 'model/encoder.pkl')
""")

    # Module 3: Smarter Alternatives Engine
    add_heading_3("Module 3: Smarter Alternatives Recommender Engine")
    add_p("The recommender engine (`utils/recommender.py`) identifies phones offering comparable or superior hardware specifications at a lower cost. Instead of returning arbitrary devices, it enforces two strict mathematical constraints:")
    add_bullet("1. Strict Price Band Filtering: Filters alternatives priced strictly between the Predicted Fair Price and the user's Current Listing Price:")
    add_p("$$\\text{Lower Bound} = \\min(P_{\\text{pred}}, P_{\\text{curr}}) \\times 0.9, \\quad \\text{Upper Bound} = \\max(P_{\\text{pred}}, P_{\\text{curr}}) \\times 1.05$$")
    add_bullet("2. Multi-Criteria Penalty Distance Function: Computes a composite penalty score prioritizing minimal price deviation from fair value while rewarding superior RAM and Storage:")
    add_p("$$\\text{Penalty} = \\frac{|P_{\\text{alt}} - P_{\\text{pred}}|}{P_{\\text{pred}}} + \\text{Penalty}_{\\text{RAM}} + \\text{Penalty}_{\\text{Storage}}$$")
    add_code_block("""# utils/recommender.py (Penalty-Ranked Alternative Recommendation)
def get_alternatives(input_specs, current_price, predicted_price, num_alternatives=10):
    df = load_data('dataset/smartphones.csv')
    ram = float(input_specs.get('RAM', 0))
    storage = float(input_specs.get('Storage', 0))
    
    # Exclude the exact phone being evaluated
    df = df[~((df['Brand'] == input_specs.get('Brand')) & (df['Model'] == input_specs.get('Model')))]
    
    lower_bound = min(predicted_price, current_price) * 0.9
    upper_bound = max(predicted_price, current_price) * 1.05
    
    # Filter by price range and spec threshold
    mask = ((df['Price'] >= lower_bound) & (df['Price'] <= upper_bound) & 
            (df['RAM'] >= max(2, ram - 2)) & (df['Storage'] >= max(16, storage / 2)))
    alternatives = df[mask].copy()
    
    def calculate_penalty(row):
        price_penalty = abs(row['Price'] - predicted_price) / predicted_price
        ram_diff = row['RAM'] - ram
        ram_penalty = abs(ram_diff) * 0.2 if ram_diff < 0 else ram_diff * 0.05
        storage_diff = row['Storage'] - storage
        storage_penalty = (abs(storage_diff)/storage)*0.2 if storage_diff < 0 else (storage_diff/storage)*0.05
        return price_penalty + ram_penalty + storage_penalty
        
    alternatives['Penalty'] = alternatives.apply(calculate_penalty, axis=1)
    alternatives = alternatives.sort_values(by='Penalty', ascending=True)
    return alternatives.drop_duplicates(subset=['Brand', 'Model']).head(num_alternatives)
""")

    # Module 4: Confidence Scorer
    add_heading_3("Module 4: Dynamic Heuristic Model Confidence Scorer")
    add_p("Rather than presenting a static confidence number, the confidence scoring engine (`utils/predictor.py`) dynamically computes confidence bounded strictly between 65% and 96% based on dataset density:")
    add_p("$$\\text{Confidence} = 65.0 + \\min\\left(10, \\frac{N_{\\text{brand}}}{40} \\times 10\\right) + \\min\\left(10, \\frac{N_{\\text{specs}}}{60} \\times 10\\right) + \\min\\left(11, \\frac{N_{\\text{proc}}}{30} \\times 11\\right)$$")
    add_code_block("""# utils/predictor.py (Bounded Dynamic Confidence Scorer)
def calculate_confidence(input_data):
    df = load_data('dataset/smartphones.csv')
    brand = input_data.get('Brand', '')
    ram = float(input_data.get('RAM', 0))
    storage = float(input_data.get('Storage', 0))
    processor = str(input_data.get('Processor', ''))
    
    brand_matches = (df['Brand'] == brand).sum()
    spec_matches = ((df['RAM'] == ram) & (df['Storage'] == storage)).sum()
    proc_tier = " ".join(processor.split()[:2]) if len(processor.split()) >= 2 else processor
    proc_matches = df['Processor'].str.contains(proc_tier, case=False, na=False).sum()
    
    confidence = 65.0
    confidence += min(10.0, (brand_matches / 40.0) * 10.0)
    confidence += min(10.0, (spec_matches / 60.0) * 10.0)
    confidence += min(11.0, (proc_matches / 30.0) * 11.0)
    
    return max(65, min(96, int(round(confidence))))
""")

    # Module 5: Flask Backend & SQLite Persistence
    add_heading_3("Module 5: Flask Backend Controllers & SQLite Persistence Architecture")
    add_p("The Flask application server (`app.py`) coordinates request routing, machine learning inference dispatching, and SQLite database transactions using parameterized SQL queries.")
    add_code_block("""# app.py (REST API Endpoints and Database Persistence)
from flask import Flask, render_template, request, jsonify, g
import sqlite3
from utils.predictor import predict_price
from utils.recommender import get_alternatives
from utils.preprocessing import get_dynamic_maps

app = Flask(__name__)
app.config['DATABASE'] = 'worthit.db'

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    prediction_result = predict_price(data)
    alternatives = get_alternatives(
        data, prediction_result['Current Price'], prediction_result['Predicted Fair Price']
    )
    return jsonify({'prediction': prediction_result, 'alternatives': alternatives})

@app.route('/saved', methods=['GET', 'POST'])
def saved():
    db = get_db()
    if request.method == 'POST':
        data = request.json
        db.execute('''INSERT INTO saved_phones 
            (brand, model, processor, ram, storage, predicted_price, current_price, savings)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (
            data.get('Brand'), data.get('Model'), data.get('Processor'),
            data.get('RAM'), data.get('Storage'), data.get('Predicted_Price'),
            data.get('Current_Price'), data.get('Savings')
        ))
        db.commit()
        return jsonify({'status': 'success'})
    cur = db.execute('SELECT * FROM saved_phones ORDER BY timestamp DESC')
    return render_template('saved.html', saved_items=[dict(r) for r in cur.fetchall()])
""")

    # Module 6: UI & Card Differentiation
    add_heading_3("Module 6: Interactive Front-End Web Architecture & Card Styling")
    add_p("The front-end user interface utilizes a modern dark/warm glassmorphism aesthetic with a terracotta/gold color palette. To clearly distinguish recommendation quality, the top 1-3 best matches from the recommender engine are rendered with a distinct visual treatment (terracotta/gold accent border and 'Best Match' badge) while rank 4+ items appear in standard card formatting.")

    # =========================================================================
    # CHAPTER 9
    # =========================================================================
    add_heading_1("CHAPTER 9: SPECIAL / CHALLENGING EXPERIENCES ENCOUNTERED DURING TRAINING")
    add_heading_2("9.1 Technical Challenges Solved")
    add_bullet("Challenge 1: Resolving Model Name Duplication in Dataset Variants", bold_prefix="")
    add_p("Problem: In early iterations of the dataset, storage capacities were baked into model names (e.g., 'iPhone 11 64GB', 'iPhone 11 128GB'), causing duplicated entries in dropdowns.\nSolution: Standardized model naming across the 2,983 records and designed `get_dynamic_maps()` to dynamically group variants under a single unique model name with separate RAM/Storage options.")
    
    add_bullet("Challenge 2: Multi-Criteria Alternative Price Band Calibration", bold_prefix="")
    add_p("Problem: The initial recommender returned phones with negligible price differences (saving Rs. 1 to Rs. 10) or wildly dissimilar specifications.\nSolution: Implemented a bounded price-band window ([P_pred * 0.9, P_curr * 1.05]) combined with a three-factor penalty function balancing fair price proximity and hardware parity.")

    add_bullet("Challenge 3: Dynamic Model Confidence Score Heuristic", bold_prefix="")
    add_p("Problem: Displaying a fixed arbitrary confidence score (e.g., 80%) lacked statistical credibility.\nSolution: Engineered a dynamic density heuristic evaluating brand representation, RAM/Storage commonality, and processor family frequency, strictly bounded between 65% and 96%.")

    # =========================================================================
    # CHAPTER 10
    # =========================================================================
    add_heading_1("CHAPTER 10: CONCLUSION")
    add_heading_2("10.1 Summary of Practical Outcomes and Experience")
    add_p("The six-week industrial training program completed at InfoStack Software Development, Training and Research Center, Solapur provided invaluable hands-on experience in full-stack data science, applied machine learning, and modern web application development. Developing the complete 'WorthIt' smartphone valuation and recommendation system solidified end-to-end competencies: data cleansing with Pandas, multi-dimensional array operations with NumPy, gradient boosted regression with XGBoost, REST API engineering with Flask, relational persistence with SQLite, and responsive UI design with modern CSS and vanilla JavaScript.")

    add_heading_2("10.2 Value Addition to Academic and Professional Development")
    add_p("The experience bridged classroom theoretical knowledge with commercial software development standards. Working in a structured engineering environment enhanced technical problem-solving capabilities, code refactoring habits, testing rigor, and workplace safety awareness, preparing the candidate for professional software engineering and machine learning roles.")

    # =========================================================================
    # CHAPTER 11
    # =========================================================================
    add_heading_1("CHAPTER 11: REFERENCES / SOURCES OF INFORMATION")
    add_bullet("Chen, T., & Guestrin, C. (2016). XGBoost: A Scalable Tree Boosting System. Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining.")
    add_bullet("McKinney, W. (2022). Python for Data Analysis: Data Wrangling with pandas, NumPy, and Jupyter (3rd ed.). O'Reilly Media.")
    add_bullet("Grinberg, M. (2018). Flask Web Development: Developing Web Applications with Python (2nd ed.). O'Reilly Media.")
    add_bullet("Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. Journal of Machine Learning Research, 12, 2825-2830.")
    add_bullet("Mozilla Developer Network (MDN). JavaScript (ES6+), DOM Manipulation, and Fetch API Technical Guides.")
    add_bullet("SQLite Documentation. An Embeddable SQL Database Engine Specification and Query Optimization Guidelines.")
    add_bullet("Maharashtra State Board of Technical Education (MSBTE). Industrial Training Manual and Guidelines for Diploma Programs, Mumbai.")
    add_bullet("InfoStack Software Development, Training and Research Center, Solapur. Technical Documentation and Training Modules (2026-2027).")

    # Save document
    output_filename = "Industrial_Training_Report_WorthIt_ML_Project.docx"
    doc.save(output_filename)
    print(f"Report generated successfully as {output_filename}")
    try:
        doc.save("Python_Data_Analysis_Machine_Learning_Industrial_Training_Report.docx")
        print("Also saved as Python_Data_Analysis_Machine_Learning_Industrial_Training_Report.docx")
    except Exception as e:
        print(f"Note: Could not overwrite existing file (it may be open in Word): {e}")

if __name__ == "__main__":
    generate_report()
