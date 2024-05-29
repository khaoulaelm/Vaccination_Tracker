import sqlite3

def setup_database():
    conn = sqlite3.connect("Vaccination Tracker.db")
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Parents (
        ParentID INTEGER PRIMARY KEY AUTOINCREMENT,
        FirstName TEXT NOT NULL,
        LastName TEXT NOT NULL,
        Email TEXT NOT NULL UNIQUE,
        Password TEXT NOT NULL,
        PhoneNumber TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Children (
        ChildID INTEGER PRIMARY KEY AUTOINCREMENT,
        ParentID INTEGER,
        FirstName TEXT NOT NULL,
        LastName TEXT NOT NULL,
        DateOfBirth DATE NOT NULL,
        FOREIGN KEY (ParentID) REFERENCES Parents (ParentID)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Vaccinations (
        Name TEXT NOT NULL,
        Description TEXT,
        AgeRecommended INTEGER,
        AgeEndRecommended INTEGER
    )
    ''')

    # Insert initial data
    cursor.execute('''
        INSERT INTO Parents (FirstName, LastName, Email, Password, PhoneNumber)
        VALUES 
        ('mariam', 'madori', 'mariam.mad@gmail.com', 'mariam.1', '0032488888888')
    ''')

    cursor.execute('''
        INSERT INTO Children (ParentID, FirstName, LastName, DateOfBirth)
        VALUES (1, 'Hajar', 'elma', '2024-03-29')
    ''')

    cursor.execute('''
        INSERT INTO Vaccinations (Name, Description, AgeRecommended, AgeEndRecommended)
        VALUES 
        ('Hepatitis B Dose 1', 'Contagious viral infection of the liver; spread through contact with infected body fluids such as blood or semen', 0, 0),
        ('Hepatitis B Dose 2', 'Contagious viral infection of the liver; spread through contact with infected body fluids such as blood or semen', 1 ,2),
        ('Hepatitis B Dose 3', 'Contagious viral infection of the liver; spread through contact with infected body fluids such as blood or semen', 6, 18),
        ('Rotavirus dose 1', 'Contagious viral infection of the gut; spread through the mouth from hands and food contaminated with stool', 2, 2),
        ('Rotavirus dose 2', 'Contagious viral infection of the gut; spread through the mouth from hands and food contaminated with stool', 4, 4),
        ('DTaP dose 1', 'protects against tetanus, diphtheria, and pertussis', 2, 2),
        ('DTaP dose 2', 'protects against tetanus, diphtheria, and pertussis', 4, 4),
        ('DTaP dose 3', 'protects against tetanus, diphtheria, and pertussis', 6, 6),
        ('DTaP dose 4', 'protects against tetanus, diphtheria, and pertussis', 15, 18),
        ('DTaP dose 5', 'protects against tetanus, diphtheria, and pertussis', 4*12, 6*12),
        ('Hib dose 1', 'Contagious bacterial infection of the lungs, brain and spinal cord, or bloodstream; spread through air and direct contact', 2, 2),
        ('Hib dose 2', 'Contagious bacterial infection of the lungs, brain and spinal cord, or bloodstream; spread through air and direct contact', 4, 4),
        ('Hib dose 3', 'Contagious bacterial infection of the lungs, brain and spinal cord, or bloodstream; spread through air and direct contact', 12, 15),
        ('Pneumococcal dose 1', 'Bacterial infections of ears, sinuses, lungs, or bloodstream; spread through direct contact with respiratory droplets like saliva or mucus', 2, 2),
        ('Pneumococcal dose 2', 'Bacterial infections of ears, sinuses, lungs, or bloodstream; spread through direct contact with respiratory droplets like saliva or mucus', 4, 4),
        ('Pneumococcal dose 3', 'Bacterial infections of ears, sinuses, lungs, or bloodstream; spread through direct contact with respiratory droplets like saliva or mucus', 6, 6),
        ('Pneumococcal dose 4', 'Bacterial infections of ears, sinuses, lungs, or bloodstream; spread through direct contact with respiratory droplets like saliva or mucus', 12, 15),
        ('Polio dose 1', 'Contagious viral infection of nerves and brain; spread through the mouth from stool on contaminated hands,food or liquid, and by air and direct contact', 2, 2),
        ('Polio dose 2', 'Contagious viral infection of nerves and brain; spread through the mouth from stool on contaminated hands,food or liquid, and by air and direct contact', 4, 4),
        ('Polio dose 3', 'Contagious viral infection of nerves and brain; spread through the mouth from stool on contaminated hands,food or liquid, and by air and direct contact', 6,18),
        ('Polio dose 4', 'Contagious viral infection of nerves and brain; spread through the mouth from stool on contaminated hands,food or liquid, and by air and direct contact', 4*12, 6*12),
        ('MMR dose 1', 'protects against measles, mumps, and rubella', 12, 15),
        ('MMR dose 2', 'protects against measles, mumps, and rubella', 4*12, 6*12)
                   
    ''')

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    setup_database()
