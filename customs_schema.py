from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import json

@dataclass
class Adresse:
    strasse: Optional[str] = None
    plz: Optional[str] = None
    ort: Optional[str] = None
    land: Optional[str] = None

@dataclass
class Ansprechpartner:
    ansprechName: Optional[str] = None
    phone: Optional[str] = None
    ansprechEmail: Optional[str] = None

@dataclass
class Nachrichtensender:
    eoriNiederlassungsnummer: Optional[str] = None

@dataclass
class Nachrichtenempfanger:
    dienststellennummer: Optional[str] = None

@dataclass
class Kopf:
    lrn: Optional[str] = None
    artderAnmeldung: Optional[str] = None
    artderAusfuhranmeldung: Optional[str] = None
    beteiligtenKonstellation: Optional[str] = None
    zeitpunktderAnmeldung: Optional[str] = None
    massgeblichesDatum: Optional[str] = None
    kopfDatumdesAusgangs: Optional[str] = None
    zeitpunktDerGestellung: Optional[str] = None
    zeitpunktdesEndesderLadetatigkeit: Optional[str] = None
    sicherheit: Optional[str] = None
    besondereUmstande: Optional[str] = None
    inRechnunggestellterGesamtbetrag: Optional[str] = None
    rechnungswahrung: Optional[str] = None

@dataclass
class Bewilligung:
    sequenznummer: Optional[str] = None
    art: Optional[str] = None
    referenznummer: Optional[str] = None

@dataclass
class Beteiligte:
    tin: Optional[str] = None
    niederlassungsNummer: Optional[str] = None
    name: Optional[str] = None
    adresse: Optional[Adresse] = None
    ansprechpartner: Optional[Ansprechpartner] = None

@dataclass
class Lieferbedingungen:
    lieferbedingungIncotermCode: Optional[str] = None
    lieferbedingungUnLocode: Optional[str] = None
    lieferbedingungOrt: Optional[str] = None
    lieferbedingungLand: Optional[str] = None
    lieferbedingungText: Optional[str] = None

@dataclass
class Warennummer:
    unterpositionDesHarmonisiertenSystems: Optional[str] = None
    unterpositionDerKombiniertenNomenklatur: Optional[str] = None

@dataclass
class Ware:
    wareWarenbezeichnung: Optional[str] = None
    warennummer: Optional[Warennummer] = None

@dataclass
class Vermessung:
    wareRohmasse: Optional[str] = None
    wareEigenmasse: Optional[str] = None
    mengeinbesondererMabeinheit: Optional[str] = None

@dataclass
class CustomsDeclarationSchema:
    nachrichtensender: Optional[Nachrichtensender] = None
    nachrichtenempfanger: Optional[Nachrichtenempfanger] = None
    kopf: Optional[Kopf] = None
    bewilligung: Optional[Bewilligung] = None
    gestellungszollstelle: Optional[Dict[str, Any]] = None
    ausfuhrzollstelle: Optional[Dict[str, Any]] = None
    ausfuhrZollstelleFurDieErganzende: Optional[Dict[str, Any]] = None
    vorgeseheneAusgangszollstelle: Optional[Dict[str, Any]] = None
    tatsachlicheAusgangszollstelle: Optional[Dict[str, Any]] = None
    aussenwirtschaftsrechtlicherAusfuhrer: Optional[Beteiligte] = None
    ausfuhrer: Optional[Beteiligte] = None
    anmelder: Optional[Beteiligte] = None
    vertreter: Optional[Beteiligte] = None
    subunternehmer: Optional[Beteiligte] = None
    lieferung: Optional[Dict[str, Any]] = None
    sendung: Optional[Dict[str, Any]] = None
    position: Optional[List[Dict[str, Any]]] = None
    additional_fields: Optional[Dict[str, Any]] = None

class CustomsFieldMapper:
    def __init__(self):
        self.german_field_mappings = {
            # Basic identifiers
            'lrn': ['lrn', 'local reference number', 'referenznummer', 'anmeldenummer'],
            'mrn': ['mrn', 'movement reference number', 'bearbeitungsnummer'],
            'eori': ['eori', 'eori-nummer', 'eori nummer'],
            
            # Dates
            'datum': ['datum', 'date', 'zeitpunkt'],
            'anmeldedatum': ['anmeldedatum', 'declaration date', 'zeitpunkt der anmeldung'],
            'ausgangsdatum': ['ausgangsdatum', 'departure date', 'datum des ausgangs'],
            'gueltigkeitsdatum': ['gültigkeitsdatum', 'validity date', 'gultigkeitsdatum'],
            
            # Companies and persons
            'anmelder': ['anmelder', 'declarant', 'deklarant'],
            'ausfuhrer': ['ausführer', 'exporter', 'ausfuhrer'],
            'empfanger': ['empfänger', 'consignee', 'empfanger'],
            'versender': ['versender', 'consignor', 'sender'],
            'beforderer': ['beförderer', 'carrier', 'beforderer'],
            'vertreter': ['vertreter', 'representative', 'agent'],
            
            # Addresses
            'name': ['name', 'firma', 'company', 'unternehmen'],
            'strasse': ['straße', 'street', 'strasse', 'adresse'],
            'plz': ['plz', 'postal code', 'postleitzahl'],
            'ort': ['ort', 'city', 'stadt'],
            'land': ['land', 'country', 'staat'],
            
            # Contact information
            'telefon': ['telefon', 'phone', 'tel', 'telephone'],
            'email': ['email', 'e-mail', 'mail'],
            'fax': ['fax', 'telefax'],
            
            # Customs offices
            'zollstelle': ['zollstelle', 'customs office', 'zollamt'],
            'gestellungszollstelle': ['gestellungszollstelle', 'office of lodgement'],
            'ausfuhrzollstelle': ['ausfuhrzollstelle', 'office of export'],
            'ausgangszollstelle': ['ausgangszollstelle', 'office of exit'],
            
            # Goods information
            'warenbezeichnung': ['warenbezeichnung', 'description of goods', 'warenbeschreibung'],
            'warennummer': ['warennummer', 'commodity code', 'hs code', 'cn code'],
            'ursprungsland': ['ursprungsland', 'country of origin', 'herkunftsland'],
            'bestimmungsland': ['bestimmungsland', 'country of destination', 'zielland'],
            
            # Quantities and values
            'menge': ['menge', 'quantity', 'anzahl'],
            'gewicht': ['gewicht', 'weight', 'masse'],
            'rohmasse': ['rohmasse', 'gross mass', 'bruttogewicht'],
            'eigenmasse': ['eigenmasse', 'net mass', 'nettogewicht'],
            'wert': ['wert', 'value', 'betrag'],
            'waehrung': ['währung', 'currency', 'waehrung'],
            
            # Transport information
            'verkehrszweig': ['verkehrszweig', 'mode of transport', 'transportmittel'],
            'kennzeichen': ['kennzeichen', 'identification', 'nummer'],
            'containernummer': ['containernummer', 'container number'],
            'verschlussnummer': ['verschlussnummer', 'seal number'],
            
            # Documents
            'dokument': ['dokument', 'document', 'unterlage'],
            'rechnung': ['rechnung', 'invoice', 'faktura'],
            'ursprungszeugnis': ['ursprungszeugnis', 'certificate of origin'],
            'ausfuhrgenhmigung': ['ausfuhrgenehmigung', 'export licence', 'exportlizenz'],
            
            # Procedures
            'verfahren': ['verfahren', 'procedure', 'prozedur'],
            'zollverfahren': ['zollverfahren', 'customs procedure'],
            'bewilligung': ['bewilligung', 'authorization', 'genehmigung'],
            
            # Additional fields
            'bemerkungen': ['bemerkungen', 'remarks', 'hinweise'],
            'zusatzliche_angaben': ['zusätzliche angaben', 'additional information'],
            'besondere_umstande': ['besondere umstände', 'special circumstances'],
        }
        
        self.english_field_mappings = {
            # Basic identifiers
            'lrn': ['lrn', 'local reference number', 'reference number'],
            'mrn': ['mrn', 'movement reference number'],
            'eori': ['eori', 'eori number'],
            
            # Dates
            'date': ['date', 'datum'],
            'declaration_date': ['declaration date', 'lodgement date'],
            'departure_date': ['departure date', 'exit date'],
            'validity_date': ['validity date', 'expiry date'],
            
            # Companies and persons
            'declarant': ['declarant', 'declarer'],
            'exporter': ['exporter', 'shipper'],
            'consignee': ['consignee', 'receiver'],
            'consignor': ['consignor', 'sender'],
            'carrier': ['carrier', 'transport company'],
            'representative': ['representative', 'agent'],
            
            # Standard invoice fields
            'invoice_number': ['invoice number', 'invoice no', 'bill number'],
            'invoice_date': ['invoice date', 'bill date'],
            'due_date': ['due date', 'payment due'],
            'total_amount': ['total amount', 'total', 'grand total'],
            'tax_amount': ['tax amount', 'vat', 'tax'],
            'currency': ['currency', 'curr'],
            
            # Line items
            'description': ['description', 'item description'],
            'quantity': ['quantity', 'qty', 'amount'],
            'unit_price': ['unit price', 'price per unit'],
            'total_price': ['total price', 'line total'],
        }

    def get_field_patterns(self, language='both'):
        if language == 'german':
            return self.german_field_mappings
        elif language == 'english':
            return self.english_field_mappings
        else:
            combined = {}
            combined.update(self.german_field_mappings)
            combined.update(self.english_field_mappings)
            return combined

    def normalize_field_name(self, field_name: str) -> str:
        """Normalize field names for consistent mapping"""
        return field_name.lower().strip().replace(' ', '_').replace('-', '_')

    def find_matching_fields(self, extracted_text: str, language='both') -> Dict[str, List[str]]:
        """Find potential field matches in extracted text"""
        patterns = self.get_field_patterns(language)
        matches = {}
        
        text_lower = extracted_text.lower()
        
        for field, patterns_list in patterns.items():
            found_patterns = []
            for pattern in patterns_list:
                if pattern.lower() in text_lower:
                    found_patterns.append(pattern)
            
            if found_patterns:
                matches[field] = found_patterns
        
        return matches