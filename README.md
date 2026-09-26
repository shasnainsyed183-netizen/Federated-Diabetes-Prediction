# 🏥 Federated Learning for Diabetes Prediction

A privacy-preserving AI system that predicts diabetes patient readmission **without sharing any patient data** between hospitals.

## 🎯 Project Overview

This project implements **Federated Learning** combined with **Differential Privacy** to train a neural network across multiple hospitals while keeping patient data completely private. Each hospital trains locally, and only encrypted model weights are shared with the central server.

## 🔑 Key Features

- **Privacy-First:** No patient data ever leaves the hospital
- **Federated Learning:** 3 hospitals train collaboratively
- **Differential Privacy:** Gaussian noise added to model weights
- **Interactive Dashboard:** Built with Streamlit
- **Real-time Prediction:** Live patient readmission risk prediction

## 📊 Results

| Model | Accuracy | Data Shared | Privacy |
|-------|----------|-------------|---------|
| Baseline (Centralized) | 62.34% | All Data | ❌ No |
| Federated Learning | 61.95% | 0 bytes | ⚠️ Partial |
| **Federated + Differential Privacy** | **62.38%** | **0 bytes** | **✅ Yes** |

**Key Achievement:** Federated Learning with Differential Privacy achieved **higher accuracy** than the centralized baseline — while preserving complete patient privacy!

## 🛠️ Technologies Used

- **Python 3.13**
- **TensorFlow 2.21** - Neural Network
- **Pandas & NumPy** - Data Processing
- **Scikit-learn** - Preprocessing
- **Streamlit** - Interactive Dashboard

## 📁 Project Structure
