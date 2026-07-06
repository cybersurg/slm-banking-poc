\# Private Banking SLM PoC - DeepSeek-R1 Local Deployment



\## Objective

This repository demonstrates a secure, offline Proof of Concept for an automated banking email triage system. It classifies customer emails (Fraud, Loan, Balance, Complaint) and extracts structured JSON data (Account Number, Amount, Urgency) using a Small Language Model (SLM) running entirely on a local laptop.



\## Why This Matters

\- Data Privacy: All sensitive banking data (account numbers, amounts) is processed 100% locally. No data leaves the machine, ensuring GDPR and HIPAA compliance.

\- Cost-Effective: Uses a free, open-source model (DeepSeek-R1) with zero cloud API costs.

\- Low Latency: Runs on standard consumer hardware (CPU only).



\## Hardware Tested On

\- Processor: Intel Core i5-8265U @ 1.60GHz (8 CPUs)

\- RAM: 16GB DDR4

\- Storage: Models stored on D: drive (Mechanical HDD)

\- GPU: Intel UHD 620 (Disabled for inference, CPU-only mode used)



\## Setup Instructions (For Reproducing this Lab)



\### 1. Install Ollama

Download the Windows installer from \[ollama.com](https://ollama.com) and install it.



\### 2. Set Environment Variables (Windows CMD)

To save storage space on the C: drive and force CPU-only inference (to avoid GPU compatibility errors):



cmd

set OLLAMA\_MODELS=D:\\ollama\_models

set OLLAMA\_NUM\_GPU=0

