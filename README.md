# The Optimizer Dev Tool
# Group 10: The Optimizers

The Optimizer Dev Tool is an accessible performance analysis development tool designed 
for software engineering students and developers to analyze and learn about 
time complexity and runtime behavior. 

---

## Overview 

This Tkinter based GUI application allows users to: 

- Log in with a secure account
- Upload or paste main() code
- View explanations on standard time complexity algorithms
- View runtime graphs of standard Big-O time complexities 
- Run performance analysis on their code
- View estimated Big-O time complexity
- Visualize runtime trends via graph
- Save and view previous code analysis results

---

## Key Features 
### **User Accounts**
  - Create an account with username and password
  - Password securely stored with Argon2 hashing
  - User directories for file handling

### **Code Submission & Highlighting**
  - Upload code files or paste code directly
  - Code must contain a main() function
  - Code can be highlighted for selection

### **Performance Analysis**
  - An analyzer will run the user's program
  - Measures execution time
  - Estimates Big-O time complexity
  - Displays result through runtime graphs

### **Student Guidance**
  - **Standard Algorithms** reference sheet
  - **Complexities Graph** for common Big-O curves
  - **User Guide** help popup for user instructions

---

## Technical Components 
- **Language**: Python
- **GUI**: Tkinter
- **Plotting**: Matplotlib
- **Numerical & Regression**: NumPy, scikit-learn
- **Security**: Argon2-cffi for password hashing

--- 

## Installation & Use 
1. Clone the repository
2. Install required technical libraries
3. Run main.py
4. Create an account
5. On main screen:
   - Click Open File to select a code file from file explorer
   - Or paste code directly into field
6. Click Submit
   - If your program requires inputs, you will be prompted to enter them
7. The analyzer will estimate Big-O complexity and generate a runtime graph
8. Instructional Tools:
   - Standard Algorithms for time complexity reference 
   - Complexities Graph to view commong Big-O curves
   - User Guide for usage help 
