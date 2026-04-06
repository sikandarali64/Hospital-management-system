#include <stdio.h>
#include <stdlib.h>  // Required for exit()
#include <string.h>

struct patient {
    char name[100];
    int age;
    char gender[10];
};

struct doctor {
    int id;
    char name[50];
    char specialization[50];
    char contact[15];
    char availability[20];
};

// Function to add a patient
void addpatient() {
    struct patient p1;
    FILE *file;

    printf("\t\t\t\t\t************************************************\n");
    printf("\t\t\t\t\t**          HOSPITAL MANAGEMENT SYSTEM       **\n");
    printf("\t\t\t\t\t************************************************\n");
    
    printf("Enter your name: ");
    scanf("%s", p1.name); 
    
    printf("Enter your age: ");
    scanf("%d", &p1.age); 

    printf("Enter gender (male/female): ");
    scanf("%s", p1.gender);
    
    if (p1.gender[0] == 'm' || p1.gender[0] == 'M')
        printf("Welcome Mr. %s\n", p1.name);
    else if (p1.gender[0] == 'f' || p1.gender[0] == 'F')
        printf("Welcome Miss. %s\n", p1.name);
    else
        printf("Invalid Key press (m for male, f for female)\n");
    
    //open the file(patient file)
    file = fopen("patients.txt", "a");
    if (file == NULL) {
        printf("Error opening file!\n");
        return;
    }

    // File mein patient details write karna
    fprintf(file, "Name: %s, Age: %d, Gender: %s\n", p1.name, p1.age, p1.gender);

    // File close karna
    fclose(file);

    printf("\nPatient details saved successfully!\n");
    printf("\n**************************\n");
}

// Function to view patients
void viewPatients() {
    FILE *file;
   char line[100];

    // File open karna (read mode mein)
    file = fopen("patients.txt", "r");
    if (file == NULL) {
        printf("No patients found!\n");
        return;
    }

    printf("\nPatient Details:\n");
    printf("------------------------------------------------------------------_____________\n");
    // File se data read karna aur print karna
 while (fgets(line, sizeof(line), file) != NULL) {
        printf("%s", line);
    }

    // File close karna
    fclose(file);
}

// Function to add a doctor
void addDoctor() {
    struct doctor d1;
    FILE *file;

    printf("Enter doctor ID: ");
    scanf("%d", &d1.id);

    printf("Enter doctor name: ");
    scanf(" %s", d1.name);

    printf("Enter specialization: ");
    scanf(" %[^\n]", d1.specialization);

    printf("Enter contact number: ");
    scanf("%s", d1.contact);

    printf("Enter availability: ");
    scanf(" %[^\n]", d1.availability);

    // File open karna (append mode mein)
    file = fopen("doctors.txt", "a");
    if (file == NULL) {
        printf("Error opening file!\n");
        return;
    }

    // File mein doctor details write karna
    fprintf(file, "ID: %d, Name: %s, Specialization: %s, Contact: %s, Availability: %s\n",
            d1.id, d1.name, d1.specialization, d1.contact, d1.availability);

    // File close karna
    fclose(file);

    printf("\nDoctor details saved successfully!\n");
}

// Function to view doctors
void viewDoctors() {
    FILE *file;
    char line[100];

    // File open karna (read mode mein)
    file = fopen("doctors.txt", "r");
    if (file == NULL) {
        printf("No doctors found!\n");
        return;
    }

    printf("\nDoctor Details:\n");
    printf("---------------\n");

    // File se data read karna aur print karna
    while (fgets(line, sizeof(line), file) != NULL) {
        printf("%s", line);
    }

    // File close karna
    fclose(file);
}


int main() {
    int choice;
    while (1) {
        printf("\nHospital Management System\n");
        printf("1. Add Patient\n");
        printf("2. View Patients\n");
        printf("3. Add Doctor\n");
        printf("4. View Doctors\n");
        printf("5. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);
        switch (choice) {
            case 1:
                addpatient();
                break;
            case 2:
                viewPatients();
                break;
            case 3:
                addDoctor();
                break;
            case 4:
                viewDoctors();
                break;
            
            case 5:
                printf("Exiting program...\n");
                exit(0);
            default:
                printf("Invalid choice! Please try again.\n");
        }
    }
    return 0;
}
