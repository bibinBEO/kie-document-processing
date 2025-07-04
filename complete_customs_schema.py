from typing import Dict, List, Optional, Any
import json

class CompleteCustomsSchema:
    @staticmethod
    def get_empty_schema() -> Dict[str, Any]:
        """Returns the complete German customs export declaration schema with all fields"""
        return {
            "nachrichtensender": {
                "eoriNiederlassungsnummer": None
            },
            "nachrichtenempfanger": {
                "dienststellennummer": None
            },
            "kopf": {
                "lrn": None,
                "artderAnmeldung": None,
                "artderAusfuhranmeldung": None,
                "beteiligtenKonstellation": None,
                "zeitpunktderAnmeldung": None,
                "massgeblichesDatum": None,
                "kopfDatumdesAusgangs": None,
                "zeitpunktDerGestellung": None,
                "zeitpunktdesEndesderLadetatigkeit": None,
                "sicherheit": None,
                "besondereUmstande": None,
                "inRechnunggestellterGesamtbetrag": None,
                "rechnungswahrung": None
            },
            "bewilligung": {
                "sequenznummer": None,
                "art": None,
                "referenznummer": None
            },
            "gestellungszollstelle": {
                "gestellungszollstelle": None
            },
            "ausfuhrzollstelle": {
                "ausfuhrzollstelleDienststellennummer": None
            },
            "ausfuhrZollstelleFurDieErganzende": {
                "ausfuhrZollstelleFurDieErganzende": None
            },
            "vorgeseheneAusgangszollstelle": {
                "vorgeseheneAusgangszollstelleDienststellennummer": None
            },
            "tatsachlicheAusgangszollstelle": {
                "tatsachlicheAusgangszollstelleDienststellennummer": None
            },
            "aussenwirtschaftsrechtlicherAusfuhrer": {
                "tin": None,
                "niederlassungsNummer": None,
                "name": None,
                "adresse": {
                    "strasse": None,
                    "plz": None,
                    "ort": None,
                    "land": None
                }
            },
            "ausfuhrer": {
                "tin": None,
                "niederlassungsNummer": None,
                "name": None,
                "adresse": {
                    "strasse": None,
                    "plz": None,
                    "ort": None,
                    "land": None
                }
            },
            "anmelder": {
                "tin": None,
                "niederlassungsNummer": None,
                "name": None,
                "adresse": {
                    "strasse": None,
                    "plz": None,
                    "ort": None,
                    "land": None
                },
                "ansprechpartner": {
                    "ansprechName": None,
                    "phone": None,
                    "ansprechEmail": None
                }
            },
            "vertreter": {
                "tin": None,
                "niederlassungsNummer": None,
                "ansprechpartner": {
                    "ansprechName": None,
                    "phone": None,
                    "ansprechEmail": None
                }
            },
            "subunternehmer": {
                "tin": None,
                "niederlassungsNummer": None,
                "name": None,
                "adresse": {
                    "strasse": None,
                    "plz": None,
                    "ort": None,
                    "land": None
                }
            },
            "lieferung": {
                "artdesGeschafts": None,
                "ausfuhrLand": None,
                "bestimmungsLand": None,
                "lieferkettenBeteiligter": [
                    {
                        "sequenznummer": None,
                        "funktion": None,
                        "identifikationsnummer": None
                    }
                ],
                "lieferbedingungen": {
                    "lieferbedingungIncotermCode": None,
                    "lieferbedingungUnLocode": None,
                    "lieferbedingungOrt": None,
                    "lieferbedingungLand": None,
                    "lieferbedingungText": None
                },
                "passiveVeredelung": {
                    "wiedereinfuhr": [
                        {
                            "position": None,
                            "wiedereinfuhrLand": None
                        }
                    ],
                    "namlichkeitsmittel": [
                        {
                            "position": None,
                            "namlichkeitsmitteArt": None,
                            "namlichkeitsmittelTextlicheBeschreibung": None
                        }
                    ],
                    "erzeugnis": [
                        {
                            "position": None,
                            "ware": {
                                "erzeugnisWarenbezeichnung": None,
                                "warennummer": {
                                    "unterpositionDesHarmonisiertenSystems": None,
                                    "unterpositionDerKombiniertenNomenklatur": None
                                }
                            }
                        }
                    ]
                }
            },
            "vorpapier": [
                {
                    "sequenznummer": None,
                    "art": None,
                    "qualifikator": None,
                    "referenznummer": None
                }
            ],
            "unterlage": [
                {
                    "sequenznummer": None,
                    "art": None,
                    "qualifikator": None,
                    "referenznummer": None,
                    "zeilenPositionsnummer": None,
                    "name": None,
                    "datumDerAusstellung": None,
                    "gultigkeitsdatum": None
                }
            ],
            "sonstigerVerweis": [
                {
                    "sequenznummer": None,
                    "art": None,
                    "qualifikator": None,
                    "referenznummer": None
                }
            ],
            "zusatzlicherInformation": [
                {
                    "sequenznummer": None,
                    "code": None,
                    "text": None
                }
            ],
            "sendung": {
                "containerIndikator": None,
                "inlandischerVerkehrszweig": None,
                "verkehrszweigAnDerGrenze": None,
                "gesamtRohmasse": None,
                "referenznummerUCR": None,
                "registriernummerextern": None,
                "beforderer": {
                    "tin": None,
                    "niederlassungsNummer": None
                },
                "versender": {
                    "tin": None,
                    "niederlassungsNummer": None,
                    "name": None,
                    "adresse": {
                        "strasse": None,
                        "plz": None,
                        "ort": None,
                        "land": None
                    }
                },
                "empfanger": {
                    "tin": None,
                    "niederlassungsNummer": None,
                    "name": None,
                    "adresse": {
                        "strasse": None,
                        "plz": None,
                        "ort": None,
                        "land": None
                    }
                },
                "transportausrustung": [
                    {
                        "sequenznummer": None,
                        "containernummer": None,
                        "anzahlderVerschlusse": None,
                        "verschluss": [
                            {
                                "sequenznummer": None,
                                "verschlusskennzeichen": None
                            }
                        ],
                        "warenpositionsverweis": [
                            {
                                "sequenznummer": None,
                                "positionsnummer": None
                            }
                        ]
                    }
                ],
                "warenort": {
                    "warenortArtdesOrtes": None,
                    "warenortArtDerOrtsbestimmung": None,
                    "warenortBewilligungsnummer": None,
                    "warenortZusatzlicheKennung": None,
                    "warenortUnLocode": None,
                    "gnss": {
                        "warenortGnssBreite": None,
                        "warenortGnssLang": None
                    },
                    "adresse": {
                        "name": None,
                        "strasse": None,
                        "plz": None,
                        "ort": None,
                        "land": None
                    },
                    "ansprechpartner": {
                        "ansprechName": None,
                        "phone": None,
                        "ansprechEmail": None
                    }
                },
                "beforderungsmittelBeimAbgang": [
                    {
                        "sequenznummer": None,
                        "artderIdentifikation": None,
                        "kennzeichen": None,
                        "staatszugehorigkeit": None
                    }
                ],
                "beforderungsroute": [
                    {
                        "sequenznummer": None,
                        "ausgewahlteLander": None
                    }
                ],
                "grenzuberschreitendesAktivesBeforderungsmittel": {
                    "beforderungsmittelderGrenzeArt": None,
                    "beforderungsmittelderGrenzeKennzeichen": None,
                    "beforderungsmittelderGrenzeStaatszugehorigkeit": None
                },
                "transportdokument": [
                    {
                        "sequenznummer": None,
                        "art": None,
                        "qualifikator": None,
                        "referenznummer": None
                    }
                ],
                "beforderungskosten": {
                    "beforderungskostenZahlungsart": None
                }
            },
            "position": [
                {
                    "sequenznummer": None,
                    "warePositionsnummer": None,
                    "statistischerWert": None,
                    "artdesGeschafts": None,
                    "ausfuhrLand": None,
                    "referenznummerUCR": None,
                    "registriernummerextern": None,
                    "bewilligung": [
                        {
                            "sequenznummer": None,
                            "art": None,
                            "referenznummer": None,
                            "bewilligungsinhaber": None
                        }
                    ],
                    "verfahren": {
                        "beantragtesVerfahren": None,
                        "vorhergehendesVerfahren": None,
                        "zusatzlichesVerfahren": [
                            {
                                "sequenznummer": None,
                                "zusatzlichesVerfahren": None
                            }
                        ]
                    },
                    "versender": {
                        "tin": None,
                        "niederlassungsNummer": None,
                        "name": None,
                        "adresse": {
                            "strasse": None,
                            "plz": None,
                            "ort": None,
                            "land": None
                        }
                    },
                    "wareEmpfanger": {
                        "tin": None,
                        "niederlassungsNummer": None,
                        "name": None,
                        "adresse": {
                            "strasse": None,
                            "plz": None,
                            "ort": None,
                            "land": None
                        }
                    },
                    "lieferkettenBeteiligter": [
                        {
                            "sequenznummer": None,
                            "funktion": None,
                            "identifikationsnummer": None
                        }
                    ],
                    "ursprung": {
                        "ursprungsland": None,
                        "ursprungsVersendungsregion": None
                    },
                    "ware": {
                        "wareWarenbezeichnung": None,
                        "warecusnummer": None,
                        "wareWarennummerKN8": {
                            "unterpositionDesHarmonisiertenSystems": None,
                            "unterpositionDerKombiniertenNomenklatur": None
                        },
                        "tariczusatzcode": [
                            {
                                "sequenznummer": None,
                                "tariczusatzcode": None
                            }
                        ],
                        "gefahrgut": [
                            {
                                "sequenznummer": None,
                                "unnummer": None
                            }
                        ],
                        "vermessung": {
                            "wareRohmasse": None,
                            "wareEigenmasse": None,
                            "mengeinbesondererMabeinheit": None
                        }
                    },
                    "verpackung": [
                        {
                            "sequenznummer": None,
                            "artderVerpackung": None,
                            "anzahlderPackstucke": None,
                            "versandzeichen": None,
                            "packstuckverweis": {
                                "packstuckverweisPositionsnummer": None
                            }
                        }
                    ],
                    "vorpapier": [
                        {
                            "sequenznummer": None,
                            "vorpapierArt": None,
                            "vorpapierQualifikator": None,
                            "vorpapierReferenznummer": None,
                            "vorpapierPositionsnummer": None,
                            "vorpapierMabeinhet": None,
                            "vorpapierMenge": None,
                            "vorpapierZusatzlicheAngaben": None
                        }
                    ],
                    "unterlage": [
                        {
                            "sequenznummer": None,
                            "art": None,
                            "qualifikator": None,
                            "referenznummer": None,
                            "zeilenPositionsnummer": None,
                            "zusatzlicheAngaben": None,
                            "detail": None,
                            "namederausstellendenBehorde": None,
                            "datumderAusstellung": None,
                            "gultigkeitsdatum": None,
                            "mabeinheit": None,
                            "erganzendeMabeinheit": None,
                            "menge": None,
                            "wahrung": None,
                            "betrag": None
                        }
                    ],
                    "sonstigerVerweis": [
                        {
                            "sequenznummer": None,
                            "art": None,
                            "qualifikator": None,
                            "referenznummer": None,
                            "detail": None,
                            "wahrung": None,
                            "betrag": None
                        }
                    ],
                    "zusatzlicheInformationlist": [
                        {
                            "sequenznummer": None,
                            "code": None,
                            "text": None
                        }
                    ],
                    "beforderungskosten": {
                        "beforderungskostenZahlungsart": None
                    },
                    "passiveVeredelung": {
                        "standardaustauschErsatzwarenverkehr": None,
                        "datumderWiedereinfuhr": None
                    },
                    "verfahrensubergangAv": {
                        "zolllager": {
                            "zolllagerLrn": None,
                            "bewilligung": {
                                "zolllagerBewilligungArt": None,
                                "zolllagerBewilligungReferenznummer": None
                            },
                            "zolllager": [
                                {
                                    "sequenznummer": None,
                                    "zuganginatlas": None,
                                    "mrn": None,
                                    "registriernummer": None,
                                    "positionsnummer": None,
                                    "ublichebehandlung": None,
                                    "zusatzlicheangaben": None,
                                    "ware": {
                                        "warennummer": {
                                            "unterpositionDesHarmonisiertenSystems": None,
                                            "unterpositionDerKombiniertenNomenklatur": None,
                                            "taricCode": None,
                                            "nationalerZusatzcode": {
                                                "nationalerZusatzcode": None
                                            }
                                        },
                                        "abgangsmenge": {
                                            "abgangsmengeMabeinheit": None,
                                            "abgangsmengeQualifikator": None,
                                            "abgangsmengeMenge": None
                                        },
                                        "handelsmenge": {
                                            "handelsmengeMabeinheit": None,
                                            "handelsmengeQualifikator": None,
                                            "handelsmengeMenge": None
                                        }
                                    }
                                }
                            ]
                        },
                        "aktiveVeredelung": {
                            "vereinfachtErteilteBewilligung": None,
                            "bewilligung": {
                                "bewilligungArt": None,
                                "bewilligungReferenznummer": None
                            },
                            "uberwachungsZollstelle": {
                                "uberwachungsZollstelleReferenznummer": None
                            },
                            "verfahrensubergangAv": [
                                {
                                    "positionAvSequenznummer": None,
                                    "positionAvZugangInAtlas": None,
                                    "warenPositionMrn": None,
                                    "positionAvRegistriernummer": None,
                                    "positionAvPositionsnummer": None,
                                    "ware": {
                                        "positionAvWarenbezogeneAngaben": None
                                    }
                                }
                            ]
                        }
                    }
                }
            ]
        }

class CompleteFieldMapper:
    def __init__(self):
        # Comprehensive field mapping with every possible field
        self.field_mappings = {
            # Root level identifiers
            'lrn': ['lrn', 'local reference number', 'lokale referenznummer', 'referenznummer'],
            'mrn': ['mrn', 'movement reference number', 'bearbeitungsnummer'],
            'eori': ['eori', 'eori-nummer', 'eori nummer', 'tin'],
            
            # Header fields (kopf)
            'artderanmeldung': ['art der anmeldung', 'declaration type'],
            'artderausfuhranmeldung': ['art der ausfuhranmeldung', 'export declaration type'],
            'beteiligtenKonstellation': ['beteiligtenkonstellation', 'parties constellation'],
            'zeitpunktderanmeldung': ['zeitpunkt der anmeldung', 'declaration time'],
            'massgeblichesdatum': ['maßgebliches datum', 'relevant date', 'massgebliches datum'],
            'kopfdatumdesausgangs': ['kopf datum des ausgangs', 'header exit date'],
            'zeitpunktdergestellung': ['zeitpunkt der gestellung', 'lodgement time'],
            'zeitpunktdesendesderladetaetigkeit': ['zeitpunkt des endes der ladetätigkeit', 'loading end time'],
            'sicherheit': ['sicherheit', 'security'],
            'besondereumstaende': ['besondere umstände', 'special circumstances'],
            'inrechnunggestelltergesamtbetrag': ['in rechnung gestellter gesamtbetrag', 'total invoiced amount'],
            'rechnungswaehrung': ['rechnungswährung', 'invoice currency', 'rechnungswahrung'],
            
            # Parties
            'anmelder': ['anmelder', 'declarant', 'deklarant'],
            'ausfuehrer': ['ausführer', 'exporter', 'ausfuhrer'],
            'aussenwirtschaftsrechtlicherausfuehrer': ['aussenwirtschaftsrechtlicher ausführer', 'economic exporter'],
            'empfaenger': ['empfänger', 'consignee', 'empfanger'],
            'versender': ['versender', 'consignor', 'sender'],
            'befoerderer': ['beförderer', 'carrier', 'beforderer'],
            'vertreter': ['vertreter', 'representative', 'agent'],
            'subunternehmer': ['subunternehmer', 'subcontractor'],
            'wareempfaenger': ['warenempfänger', 'goods consignee', 'wareempfanger'],
            
            # Contact information
            'ansprechname': ['ansprechpartner', 'contact person', 'ansprechname'],
            'phone': ['telefon', 'phone', 'tel', 'telephone'],
            'ansprechemail': ['email', 'e-mail', 'mail', 'ansprechemail'],
            
            # Addresses
            'name': ['name', 'firma', 'company', 'unternehmen'],
            'strasse': ['straße', 'street', 'strasse', 'adresse'],
            'plz': ['plz', 'postal code', 'postleitzahl'],
            'ort': ['ort', 'city', 'stadt'],
            'land': ['land', 'country', 'staat'],
            
            # Customs offices
            'gestellungszollstelle': ['gestellungszollstelle', 'office of lodgement'],
            'ausfuhrzollstelle': ['ausfuhrzollstelle', 'office of export'],
            'ausfuhrzollstellefuerdieergaenzende': ['ausfuhrzollstelle für die ergänzende', 'supplementary export office'],
            'vorgeseheneausgangszollstelle': ['vorgesehene ausgangszollstelle', 'intended office of exit'],
            'tatsaechlicheausgangszollstelle': ['tatsächliche ausgangszollstelle', 'actual office of exit'],
            'dienststellennummer': ['dienststellennummer', 'office number'],
            
            # Authorization
            'bewilligung': ['bewilligung', 'authorization', 'genehmigung'],
            'bewilligungsinhaber': ['bewilligungsinhaber', 'authorization holder'],
            'sequenznummer': ['sequenznummer', 'sequence number'],
            'art': ['art', 'type', 'typ'],
            'referenznummer': ['referenznummer', 'reference number'],
            
            # Delivery/shipment
            'artdesgeschaefts': ['art des geschäfts', 'nature of transaction'],
            'ausfuhrland': ['ausfuhrland', 'export country'],
            'bestimmungsland': ['bestimmungsland', 'destination country'],
            'ursprungsland': ['ursprungsland', 'country of origin'],
            'ursprungsversendungsregion': ['ursprungsversendungsregion', 'origin dispatch region'],
            
            # Incoterms
            'lieferbedingungincotermcode': ['lieferbedingung incoterm code', 'incoterm code'],
            'lieferbedingungunlocode': ['lieferbedingung un locode', 'incoterm location code'],
            'lieferbedingungort': ['lieferbedingung ort', 'incoterm place'],
            'lieferbedingungland': ['lieferbedingung land', 'incoterm country'],
            'lieferbedingungtext': ['lieferbedingung text', 'incoterm text'],
            
            # Transport
            'containerindikator': ['containerindikator', 'container indicator'],
            'inlaendischervehrkehrszweig': ['inländischer verkehrszweig', 'inland mode of transport'],
            'verkehrszweiganddergrenze': ['verkehrszweig an der grenze', 'mode of transport at border'],
            'gesamtrohmasse': ['gesamtrohmasse', 'total gross mass'],
            'referenznummerucr': ['referenznummer ucr', 'ucr reference'],
            'registriernummerextern': ['registriernummer extern', 'external registration'],
            'containernummer': ['containernummer', 'container number'],
            'verschlusskennzeichen': ['verschlusskennzeichen', 'seal identifier'],
            'anzahlderverschluesse': ['anzahl der verschlüsse', 'number of seals'],
            'kennzeichen': ['kennzeichen', 'identification'],
            'staatszugehoerigkeit': ['staatszugehörigkeit', 'nationality'],
            'artderidentifikation': ['art der identifikation', 'type of identification'],
            
            # Goods information
            'warenbezeichnung': ['warenbezeichnung', 'description of goods', 'warenbeschreibung'],
            'erzeugniswarenbezeichnung': ['erzeugnis warenbezeichnung', 'product description'],
            'warennummer': ['warennummer', 'commodity code', 'hs code', 'cn code'],
            'warewarennummerkn8': ['ware warennummer kn8', 'cn8 commodity code'],
            'warecusnummer': ['ware cusnummer', 'customs code'],
            'unterpositiondesharmonisiertensystems': ['unterposition des harmonisierten systems', 'hs subheading'],
            'unterpositionderkombiniertennomenklatur': ['unterposition der kombinierten nomenklatur', 'cn subheading'],
            'tariccode': ['taric code', 'taric'],
            'tariczusatzcode': ['taric zusatzcode', 'additional taric code'],
            'nationalerzusatzcode': ['nationaler zusatzcode', 'national additional code'],
            
            # Quantities and measures
            'warepositionsnummer': ['warenpositionsnummer', 'item number'],
            'statistischerwert': ['statistischer wert', 'statistical value'],
            'wareigenrasse': ['ware rohmasse', 'gross mass'],
            'wareeigenmasse': ['ware eigenmasse', 'net mass'],
            'mengeinbesonderermasseinheit': ['menge in besonderer maßeinheit', 'quantity in supplementary unit'],
            'menge': ['menge', 'quantity', 'anzahl'],
            'mabeinheit': ['maßeinheit', 'unit of measure', 'mabeinheit'],
            'ergaenzendermabeinheit': ['ergänzende maßeinheit', 'supplementary unit'],
            'abgangsmenge': ['abgangsmenge', 'departure quantity'],
            'handelsmenge': ['handelsmenge', 'commercial quantity'],
            'abgangsmengrmabeinheit': ['abgangsmenge maßeinheit', 'departure quantity unit'],
            'abgangsmengequalifikator': ['abgangsmenge qualifikator', 'departure quantity qualifier'],
            'abgangsmengermenge': ['abgangsmenge menge', 'departure quantity amount'],
            'handelsmengermabeinheit': ['handelsmenge maßeinheit', 'commercial quantity unit'],
            'handelsmengequalifikator': ['handelsmenge qualifikator', 'commercial quantity qualifier'],
            'handelsmengermenge': ['handelsmenge menge', 'commercial quantity amount'],
            
            # Values and currency
            'betrag': ['betrag', 'amount', 'wert'],
            'waehrung': ['währung', 'currency', 'waehrung'],
            
            # Packaging
            'artderverpackung': ['art der verpackung', 'type of packages'],
            'anzahlderpackstuecke': ['anzahl der packstücke', 'number of packages'],
            'versandzeichen': ['versandzeichen', 'shipping marks'],
            'packstuckverweispositionsnummer': ['packstückverweis positionsnummer', 'package reference item number'],
            
            # Documents
            'vorpapier': ['vorpapier', 'previous document'],
            'unterlage': ['unterlage', 'document'],
            'transportdokument': ['transportdokument', 'transport document'],
            'sonstigerverweis': ['sonstiger verweis', 'other reference'],
            'qualifikator': ['qualifikator', 'qualifier'],
            'zeilenpositionsnummer': ['zeilenpositionsnummer', 'line item number'],
            'datumderausstellung': ['datum der ausstellung', 'issue date'],
            'gultigkeitsdatum': ['gültigkeitsdatum', 'validity date'],
            'namederausstellendenbehorde': ['name der ausstellenden behörde', 'issuing authority'],
            'zusaetzlicheangaben': ['zusätzliche angaben', 'additional information'],
            'detail': ['detail', 'details'],
            
            # Additional information
            'zusaetzlicheinformation': ['zusätzliche information', 'additional information'],
            'code': ['code', 'kode'],
            'text': ['text', 'beschreibung'],
            
            # Procedures
            'verfahren': ['verfahren', 'procedure'],
            'beantragtesverfahren': ['beantragtes verfahren', 'requested procedure'],
            'vorhergehendesverfahren': ['vorhergehendes verfahren', 'previous procedure'],
            'zusaetzlichesverfahren': ['zusätzliches verfahren', 'additional procedure'],
            
            # Location of goods
            'warenort': ['warenort', 'location of goods'],
            'warenortartdesortes': ['warenort art des ortes', 'location type'],
            'warenortartderortsbestimmung': ['warenort art der ortsbestimmung', 'location identification type'],
            'warenortbewilligungsnummer': ['warenort bewilligungsnummer', 'location authorization number'],
            'warerortzusaetzlichekennung': ['warenort zusätzliche kennung', 'location additional identifier'],
            'warenortunlocode': ['warenort un locode', 'location un locode'],
            'warenortgnssbreite': ['warenort gnss breite', 'location gnss latitude'],
            'warenortgnsslang': ['warenort gnss länge', 'location gnss longitude'],
            
            # Transport equipment
            'transportausruestung': ['transportausrüstung', 'transport equipment'],
            'verschluss': ['verschluss', 'seal'],
            'warenpositionsverweis': ['warenpositionsverweis', 'goods item reference'],
            'positionsnummer': ['positionsnummer', 'item number'],
            
            # Transport means
            'befoerderungsmittelbeimabgang': ['beförderungsmittel beim abgang', 'means of transport at departure'],
            'grenzueberschreitendesaktivesbefoerderungsmittel': ['grenzüberschreitendes aktives beförderungsmittel', 'active means of transport crossing border'],
            'befoerderungsmitteldergrenzeart': ['beförderungsmittel der grenze art', 'border transport type'],
            'befoerderungsmitteldergrenzekennzeichen': ['beförderungsmittel der grenze kennzeichen', 'border transport identifier'],
            'befoerderungsmitteldergrenzesstaatszugehoerigkeit': ['beförderungsmittel der grenze staatszugehörigkeit', 'border transport nationality'],
            
            # Routes
            'befoerderungsroute': ['beförderungsroute', 'transport route'],
            'ausgewaehltelaender': ['ausgewählte länder', 'selected countries'],
            
            # Transport costs
            'befoerderungskosten': ['beförderungskosten', 'transport charges'],
            'befoerderungskostenzahlungsart': ['beförderungskosten zahlungsart', 'transport charges payment method'],
            
            # Dangerous goods
            'gefahrgut': ['gefahrgut', 'dangerous goods'],
            'unnummer': ['un nummer', 'un number'],
            
            # Supply chain
            'lieferkettenbeteiligter': ['lieferkettenbeteiligter', 'supply chain actor'],
            'funktion': ['funktion', 'function'],
            'identifikationsnummer': ['identifikationsnummer', 'identification number'],
            
            # Passive processing
            'passiveveredelung': ['passive veredelung', 'inward processing'],
            'wiedereinfuhr': ['wiedereinfuhr', 're-import'],
            'wiedereinfuhrland': ['wiedereinfuhr land', 're-import country'],
            'naemlichkeitsmittel': ['nämlichkeitsmittel', 'identification means'],
            'naemlichkeitsmitteart': ['nämlichkeitsmittel art', 'identification means type'],
            'naemlichkeitsmitteltextlichebeschreibung': ['nämlichkeitsmittel textliche beschreibung', 'identification means description'],
            'erzeugnis': ['erzeugnis', 'product'],
            'standardaustauschersatzwarenverkehr': ['standardaustausch ersatzwarenverkehr', 'standard exchange equivalent goods'],
            'datumdarwiedereinfuhr': ['datum der wiedereinfuhr', 're-import date'],
            
            # Warehouse procedure
            'verfahrensubergangav': ['verfahrensübergang av', 'procedure transition'],
            'zolllager': ['zolllager', 'customs warehouse'],
            'zolllgerlrn': ['zolllager lrn', 'warehouse lrn'],
            'zolllgerbewilligungsnummer': ['zolllager bewilligungsnummer', 'warehouse authorization number'],
            'zolllgerbewilligungart': ['zolllager bewilligung art', 'warehouse authorization type'],
            'zolllgerbewilligungreferenznummer': ['zolllager bewilligung referenznummer', 'warehouse authorization reference'],
            'zuganginatlas': ['zugang in atlas', 'access in atlas'],
            'registriernummer': ['registriernummer', 'registration number'],
            'ueblichebehandlung': ['übliche behandlung', 'usual treatment'],
            'zusaetzlicheangaben': ['zusätzliche angaben', 'additional information'],
            
            # Active processing
            'aktiveveredelung': ['aktive veredelung', 'outward processing'],
            'vereinfachterteilbewilligung': ['vereinfacht erteilte bewilligung', 'simplified authorization'],
            'ueberwachungszollstelle': ['überwachungszollstelle', 'supervising customs office'],
            'ueberwachungszollstellereferenznummer': ['überwachungszollstelle referenznummer', 'supervising office reference'],
            'positionavsequenznummer': ['position av sequenznummer', 'position sequence number'],
            'positionavzugangppatlas': ['position av zugang in atlas', 'position access in atlas'],
            'warenpositionmrn': ['warenposition mrn', 'goods item mrn'],
            'positionavregistriernummer': ['position av registriernummer', 'position registration number'],
            'positionavpositionsnummer': ['position av positionsnummer', 'position item number'],
            'positionavwarenbezogeneangaben': ['position av warenbezogene angaben', 'position goods-related information'],
            
            # Misc document fields
            'vorpapierart': ['vorpapier art', 'previous document type'],
            'vorpapierqualifikator': ['vorpapier qualifikator', 'previous document qualifier'],
            'vorpapierreferenznummer': ['vorpapier referenznummer', 'previous document reference'],
            'vorpapierpositionsnummer': ['vorpapier positionsnummer', 'previous document item number'],
            'vorpapiermabeinheit': ['vorpapier maßeinheit', 'previous document unit'],
            'vorpapiermenge': ['vorpapier menge', 'previous document quantity'],
            'vorpapierzusaetzlicheangaben': ['vorpapier zusätzliche angaben', 'previous document additional information']
        }
    
    def get_all_field_patterns(self) -> Dict[str, List[str]]:
        return self.field_mappings
    
    def normalize_field_name(self, field_name: str) -> str:
        """Normalize field names for consistent mapping"""
        normalized = field_name.lower().strip()
        normalized = normalized.replace(' ', '').replace('-', '').replace('_', '')
        normalized = normalized.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')
        return normalized
    
    def find_best_field_match(self, extracted_field: str) -> Optional[str]:
        """Find the best matching schema field for an extracted field"""
        normalized_extracted = self.normalize_field_name(extracted_field)
        
        best_match = None
        best_score = 0
        
        for schema_field, patterns in self.field_mappings.items():
            for pattern in patterns:
                normalized_pattern = self.normalize_field_name(pattern)
                
                # Exact match
                if normalized_extracted == normalized_pattern:
                    return schema_field
                
                # Substring match
                if normalized_pattern in normalized_extracted or normalized_extracted in normalized_pattern:
                    score = len(normalized_pattern)
                    if score > best_score:
                        best_score = score
                        best_match = schema_field
        
        return best_match