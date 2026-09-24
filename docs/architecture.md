# Architecture

This repository is a sanitized public portfolio implementation of a document-AI workflow for structured processing of EOB-style documents.

## Flow

~~~text
PDF document
    |
    v
pdfplumber text extraction
    |
    +--> PyMuPDF fallback when needed
    |
    v
Structured extraction
    |
    +--> deterministic parser for reproducible demo
    |
    +--> optional Claude API provider
    |
    v
Field validation
    |
    v
Business Central field mapping
    |
    v
Excel export
~~~

## Engineering decisions

- Public tests use synthetic EOB text, not patient or employer records.
- PDF extraction is isolated from field parsing.
- Claude is optional and is never called during CI.
- Required-field validation happens before downstream mapping.
- Credentials belong in environment variables and are never committed.
