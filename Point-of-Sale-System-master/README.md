# Legacy POS System

This directory contains the **original legacy Java-based desktop Point-of-Sale (POS) system** that was reengineered into the modern web application.

## 📋 Overview

This is the **before** version of the system - a desktop application built with:
- **Language:** Java
- **UI Framework:** Java Swing
- **Data Storage:** Plain text files
- **Architecture:** Monolithic (3 layers)
- **Deployment:** Desktop application (JAR file)

## 📁 Structure

```
Point-of-Sale-System-master/
├── src/                    # Java source code (.java files)
│   ├── POSSystem.java     # Main entry point
│   ├── PointOfSale.java   # Abstract base class
│   ├── POS.java           # Sale transactions
│   ├── POR.java           # Rental transactions
│   ├── POH.java           # Return transactions
│   ├── Inventory.java     # Inventory management
│   └── ...                # Other classes
├── Database/              # Plain text database files
│   ├── employeeDatabase.txt
│   ├── itemDatabase.txt
│   ├── userDatabase.txt
│   └── ...
├── Documentation/         # Original project documentation
│   ├── Inception Phase/
│   ├── Elaboration Phase/
│   ├── Construction Phase/
│   └── Beta Release/
├── tests/                 # Test files
└── build.xml             # Ant build configuration
```

## 🔍 Key Characteristics

### Architecture
- **Monolithic design** - All layers tightly coupled
- **File-based storage** - No database, uses plain text files
- **Single-user** - No concurrent access support
- **Desktop-only** - Java Swing GUI

### Data Storage
- **Format:** Plain text files (space-separated values)
- **No validation** - Data integrity not enforced
- **No transactions** - No ACID properties
- **Sequential reads** - O(n) performance

### Security
- **Plain text passwords** - No encryption
- **No authentication framework** - Custom implementation
- **No session management** - In-memory only

## 🔄 Comparison

See the [Legacy vs Re-engineered Comparison](../docs/LEGACY_VS_REENGINEERED_COMPARISON.md) document for a detailed side-by-side comparison.

## 📊 Reengineering Process

This legacy system was analyzed, reverse-engineered, and transformed through 9 phases:

1. **Inventory Analysis** - Cataloged all assets
2. **Document Restructuring** - Documented legacy architecture
3. **Reverse Engineering** - Extracted design patterns and code smells
4. **Code Restructuring** - Applied 9 major refactorings
5. **Data Restructuring** - Designed normalized database schema
6. **Forward Engineering** - Built modern web application
7. **Migration Strategy** - Migrated data from files to database
8. **Testing** - Created 39 automated tests
9. **Documentation** - Comprehensive documentation

## 🎯 Purpose

This legacy system is included for:
- **Reference** - Understanding what was reengineered
- **Comparison** - Side-by-side comparison with reengineered version
- **Learning** - Example of legacy system challenges
- **Documentation** - Supporting reengineering documentation

## 📝 Notes

- **Source code only** - Compiled `.class` files excluded
- **Original data files** - Sample database files included
- **Original documentation** - All project phases documented
- **Build artifacts excluded** - `.jar` files and build outputs not included

## 🔗 Related Documentation

- [Technical Report](../docs/TECHNICAL_REPORT.md) - Complete reengineering documentation
- [Legacy vs Re-engineered Comparison](../docs/LEGACY_VS_REENGINEERED_COMPARISON.md) - Detailed comparison
- [Refactoring Documentation](../docs/REFACTORING_DOCUMENTATION.md) - Code improvements
- [Work Distribution](../docs/WORK_DISTRIBUTION.md) - Team contributions

---

**Note:** This is the original legacy system. The reengineered version is in the parent directory.

