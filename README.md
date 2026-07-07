# Skill Intelligence Platform
An end-to-end Skill Intelligence Platform for resume parsing, skill extraction, normalization, and candidate-job matching using LLMs and NLP.

## Overview

Skill Intelligence Platform is an end-to-end system for extracting and normalizing skills from resumes using Large Language Models (LLMs) and Natural Language Processing (NLP).

The initial MVP focuses on transforming unstructured resume documents into structured skill representations. Future versions will extend the pipeline to job description parsing, candidate-job matching, and knowledge graph construction.

## Architecture

| Stage | Description |
|-------|-------------|
| Resume Text | Input unstructured resume text |
| Skill Extraction | Identify skills using LLMs and NER |
| Skill Normalization | Map extracted skills to standardized skill names using dictionaries, embeddings, and LLMs |
| Structured Skill JSON | Generate structured, machine-readable skill representations |

## Data

### Resume
Resume Dataset: https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset

JobHop (In the future): https://arxiv.org/abs/2505.07653

### Job
job-skill-set: https://www.kaggle.com/datasets/batuhanmutlu/job-skill-set

### Skill Taxonomy
ESCO: https://esco.ec.europa.eu/en/classification/skill_main

O*NET: https://www.onetcenter.org/database.html#overview

### Skill Extraction Evaluation
SkillSpan: https://arxiv.org/abs/2204.12811

## Acknowledgement
This project uses the ESCO classification of the European Commission.