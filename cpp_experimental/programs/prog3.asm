
// Compute division and multiplication
// Places quotent into X3 and product into X4

// Arg1 (A): Put value '50' in X1
ADDI X1, XZR, #50

// Arg2 (B): Put value '5' in X2
ADDI X2, XZR, #5



// --------------------------------------------------
// --------------------------------------------------

//
// Helper Functions
//

// Places the result of 'X2 / X3' into X1
// Caller saves X1
DIVISION:
    // Setting up output register
    ADD X1, XZR, XZR

    ADDI X1, X1, #1
    SUB X2, X2, X3
    CBNZ X2, [XZR, #-3] // Loop until X2 == 0

    JR X0 // Return to Caller

// Places the result of 'X2 * X3' into X1
// Caller saves X1
MULTIPLICATION:
    // Setting up output register
    ADD X1, XZR, XZR

    ADD X1, X1, X2
    SUBI X3, X3, #1
    CBNZ X3, [XZR, #-3] // Loop until X3 == 0

    JR X0 // Return to Caller

// --------------------------------------------------
// --------------------------------------------------



// Save scratch registers
    // Push X1 to stack - Computing results
    // Push X21 to stack - Saving Arg1
    // Push X22 to stack - Saving Arg2
    // Push X23 to stack - Storing Quotent
    // Push X24 to stack - Storing Product

// Saving Args
ADD X21, X1, XZR
ADD X22, X2, XZR

// Setting up Args for Division function call
ADD X2, X21, XZR
ADD X3, X22, XZR

// Making Division function call
JALR MULTIPLICATION

// Save Division result (X1) into X23

// Setting up Args for Multiplication function call
ADD X2, X21, XZR
ADD X3, X22, XZR

// Making Multiplication function call
JALR DIVISION

// Save Multiplication result (X1) into X24

// Placing Quotent and Reminder into X3, X4 
ADD X3, X23, XZR
ADD X4, X24, XZR

// Restoring scratch registers
    // Restore X24 from scratch
    // Restore X23 from scratch
    // Restore X22 from scratch
    // Restore X21 from scratch
    // Restore X1 from scratch

JR X0