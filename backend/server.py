from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
import uuid

# MongoDB connection
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017/')
client = MongoClient(MONGO_URL)
db = client['powerbi_directory']
reports_collection = db['reports']

# FastAPI app
app = FastAPI(title="Power BI Directory API", description="API for managing Power BI reports directory")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
reports_data = [
    {
        "id": str(uuid.uuid4()),
        "name": "Análisis Comercial",
        "group": "DIRECCION COMERCIAL",
        "url": "https://app.powerbi.com/groups/67bbc8c4-ca83-4b3d-98d1-99109d051af0/reports/aed4774c-a6dc-4acd-9977-c7246239a09c/c99aee976b06d82a1ab2?experience=power-bi",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Análisis Comercial comerciales",
        "group": "COMERCIALES",
        "url": "https://app.powerbi.com/groups/838a62aa-c347-450b-b565-bfed648f7e54/reports/bb46fc23-154e-4be1-b7d8-30f279d57f71/c99aee976b06d82a1ab2?experience=power-bi",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Castrol + Repsol + TEB + Neumáticos comerciales",
        "group": "COMERCIALES",
        "url": "https://app.powerbi.com/groups/838a62aa-c347-450b-b565-bfed648f7e54/reports/d2b119b7-3ea6-4ca5-8c32-5e9cb162ae93/c99aee976b06d82a1ab2?experience=power-bi",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Castrol + Repsol + TEB + Neumáticos",
        "group": "DIRECCION COMERCIAL",
        "url": "https://app.powerbi.com/groups/67bbc8c4-ca83-4b3d-98d1-99109d051af0/reports/594ef6f9-298f-4316-8894-df5e3c9aa141/ac5721623503d4cd0686?experience=power-bi",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Centralita Telefónica",
        "group": "SUCURSALES",
        "url": "https://app.powerbi.com/groups/d66aa69b-25dc-4f87-b07c-75940a054046/reports/74df4ef8-0532-4054-ba18-261a751281df/3116b5bd26a444d82216?experience=power-bi",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Cobros Pdtes Empleados",
        "group": "RECURSOS HUMANOS",
        "url": "https://app.powerbi.com/groups/a6f47814-ba49-468b-9dd8-e08a38b2a0fb/reports/226f2162-d580-4bbe-92ca-761bfd27556d/d1445860542d9a23f675?experience=power-bi",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Cobros y Pagos Bancos",
        "group": "GERENCIA",
        "url": "https://app.powerbi.com/groups/cdb9df2c-4dfa-4824-888d-26de261e1c52/reports/fb51cdde-1228-4e4c-ac31-72fbe0a5e2a8/d1445860542d9a23f675?experience=power-bi",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Contable Grupo Salas Automoción (ISI)",
        "group": "DIRECCION COMERCIAL",
        "url": "https://app.powerbi.com/groups/67bbc8c4-ca83-4b3d-98d1-99109d051af0/reports/00519e03-b2cc-4c6c-b04b-3849e2cd60ce/ReportSectionf3e2f71104e7ecb2b1c8?experience=power-bi",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Control de Pedidos Enviados",
        "group": "COMPRAS",
        "url": "https://app.powerbi.com/groups/d44fd147-5c8a-49c9-b666-27039a11f888/reports/0cda9ca5-0b2b-41f8-ab2a-2351add4219e/ff406f18f8389418289c?experience=power-bi",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Control de Proveedores",
        "group": "COMPRAS",
        "url": "https://app.powerbi.com/groups/d44fd147-5c8a-49c9-b666-27039a11f888/reports/f0c2f731-9259-40d4-99c3-d7fae667a8fa/ff406f18f8389418289c?experience=power-bi",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Control de Riesgos",
        "group": "DIRECCION COMERCIAL",
        "url": "https://app.powerbi.com/groups/67bbc8c4-ca83-4b3d-98d1-99109d051af0/reports/7fc41a7a-bf35-4178-afc4-a9e7aef50951/0298c2858a3e31165f74?experience=power-bi",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "DIY",
        "group": "COMERCIALES",
        "url": "https://app.powerbi.com/groups/67bbc8c4-ca83-4b3d-98d1-99109d051af0/reports/cfeb8737-840c-42f0-a659-78eb6420c913/9dcaa62f3d5351767ed4?experience=power-bi",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "DiY Compras + Tablas Básicas",
        "group": "COMPRAS",
        "url": "https://app.powerbi.com/groups/d44fd147-5c8a-49c9-b666-27039a11f888/reports/18cf3a97-9533-4d26-a971-674ad24fe004/9dcaa62f3d5351767ed4?experience=power-bi",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Estadísticas Profit comerciales",
        "group": "COMERCIALES",
        "url": "https://app.powerbi.com/groups/67bbc8c4-ca83-4b3d-98d1-99109d051af0/reports/d2ce7c81-60a6-4e8d-b099-8887859ed6c1/46d975572adac9fa7955?experience=power-bi",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Estadísticas Profit",
        "group": "DIRECCION COMERCIAL",
        "url": "https://app.powerbi.com/groups/67bbc8c4-ca83-4b3d-98d1-99109d051af0/reports/d2ce7c81-60a6-4e8d-b099-8887859ed6c1/46d975572adac9fa7955?experience=power-bi",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Faltas / Excesos en Pedidos Proveedor",
        "group": "DIRECCION COMERCIAL",
        "url": "https://app.powerbi.com/groups/67bbc8c4-ca83-4b3d-98d1-99109d051af0/reports/cf897335-4353-4589-8166-9f8b05bbead7/6f363a2de517f6e3a1f0?experience=power-bi",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Faltas / Excesos en Pedidos Proveedor comerciales",
        "group": "COMERCIALES",
        "url": "https://app.powerbi.com/groups/67bbc8c4-ca83-4b3d-98d1-99109d051af0/reports/cf897335-4353-4589-8166-9f8b05bbead7/6f363a2de517f6e3a1f0?experience=power-bi",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Garantías comerciales",
        "group": "COMERCIALES",
        "url": "https://app.powerbi.com/groups/67bbc8c4-ca83-4b3d-98d1-99109d051af0/reports/c860cdb4-545a-472e-8250-4722afdafb1f/ReportSectione1b4927968e0039ae548?experience=power-bi",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Garantías",
        "group": "DIRECCION COMERCIAL",
        "url": "https://app.powerbi.com/groups/67bbc8c4-ca83-4b3d-98d1-99109d051af0/reports/c860cdb4-545a-472e-8250-4722afdafb1f/ReportSectione1b4927968e0039ae548?experience=power-bi",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Gestión de Cobros",
        "group": "DIRECCION COMERCIAL",
        "url": "https://app.powerbi.com/groups/67bbc8c4-ca83-4b3d-98d1-99109d051af0/reports/b5117c2c-46e0-4694-9e58-7e0de0c8820d/d1445860542d9a23f675?experience=power-bi",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Gestión de Cobros comerciales",
        "group": "COMERCIALES",
        "url": "https://app.powerbi.com/groups/67bbc8c4-ca83-4b3d-98d1-99109d051af0/reports/b5117c2c-46e0-4694-9e58-7e0de0c8820d/d1445860542d9a23f675?experience=power-bi",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Informe de Ventas",
        "group": "GERENCIA",
        "url": "https://app.powerbi.com/groups/cdb9df2c-4dfa-4824-888d-26de261e1c52/reports/9ca90809-62e0-4d47-b062-89ea3af535f8/6248de83981a6fc1092d?experience=power-bi",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Informes Intranet Salas",
        "group": "RECURSOS HUMANOS",
        "url": "https://app.powerbi.com/groups/a6f47814-ba49-468b-9dd8-e08a38b2a0fb/reports/345f5abb-493e-4cb5-b793-69de8b015611/ReportSection?experience=power-bi",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Inventario 15 días",
        "group": "SUCURSALES",
        "url": "https://app.powerbi.com/groups/me/reports/b9948a08-d387-452e-a87a-12178e643883/e38ea84c0e98dd187a60?experience=power-bi",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Jornadas Técnicas",
        "group": "DIRECCION COMERCIAL",
        "url": "https://app.powerbi.com/groups/67bbc8c4-ca83-4b3d-98d1-99109d051af0/reports/e8e37d03-275e-4d7f-a7d8-100de5ffbfd5/d93ea926d138b5ad42a3?experience=power-bi",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Nueva Distribución",
        "group": "COMPRAS",
        "url": "https://app.powerbi.com/groups/d44fd147-5c8a-49c9-b666-27039a11f888/reports/476efb23-e9bd-4bfe-bdd8-b65d7312c7a8/c99aee976b06d82a1ab2?experience=power-bi",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Operaciones Vinculadas",
        "group": "GERENCIA",
        "url": "https://app.powerbi.com/groups/cdb9df2c-4dfa-4824-888d-26de261e1c52/reports/46e050d2-901f-41f1-b9f7-9e088baa78d8/007fc5865eb210a3c6db?experience=power-bi",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Pedidos a Otras Sucursales y Urgencias",
        "group": "COMPRAS",
        "url": "https://app.powerbi.com/groups/e6caf727-84e2-41a9-9e48-e626e0485463/reports/9e7eb8cd-1801-40ee-b4c1-9ef85ee43faf/ReportSection?experience=power-bi",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Presentación a Sucursales",
        "group": "DIRECCION COMERCIAL",
        "url": "https://app.powerbi.com/groups/67bbc8c4-ca83-4b3d-98d1-99109d051af0/reports/79f3de82-33b6-4922-90d5-2cfff4dd4c99/0298c2858a3e31165f74?experience=power-bi",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Presentación Liquidaciones Contratos",
        "group": "DIRECCION COMERCIAL",
        "url": "https://app.powerbi.com/groups/67bbc8c4-ca83-4b3d-98d1-99109d051af0/reports/0e1d53af-d16d-435d-abea-8966bb8483c7/8659b4c09b0408e10632?experience=power-bi",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Proyecto Elcano comerciales",
        "group": "GERENCIA",
        "url": "https://app.powerbi.com/groups/cdb9df2c-4dfa-4824-888d-26de261e1c52/reports/40f80ee9-83a1-4b99-820e-87e2ae2a64a8/7515bd041929eb0ab2ed?experience=power-bi",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Proyecto Elcano Direccion Comercial",
        "group": "COMERCIALES",
        "url": "https://app.powerbi.com/groups/838a62aa-c347-450b-b565-bfed648f7e54/reports/1d6d74ad-9250-4e9b-be85-a651a9100919/c99aee976b06d82a1ab2?experience=power-bi",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Proyecto Elcano Gerencia",
        "group": "DIRECCION COMERCIAL",
        "url": "https://app.powerbi.com/groups/67bbc8c4-ca83-4b3d-98d1-99109d051af0/reports/9f4ddd3e-e701-42a9-9e17-aeed698d393e/c99aee976b06d82a1ab2?experience=power-bi",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Reporte Diario RS",
        "group": "GERENCIA",
        "url": "https://app.powerbi.com/groups/me/reports/121ccf1b-44bb-4bb1-97b9-15f36b0b078d/f3d7273920bcfc4697a2?experience=power-bi",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Reporte Fidelización",
        "group": "DIRECCION COMERCIAL",
        "url": "https://app.powerbi.com/groups/67bbc8c4-ca83-4b3d-98d1-99109d051af0/reports/1c538db5-72f5-43ee-8287-50e3cc2a4321/43b489d0b6c015c0abc0?experience=power-bi",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Reportes AD",
        "group": "COMPRAS",
        "url": "https://app.powerbi.com/groups/d44fd147-5c8a-49c9-b666-27039a11f888/reports/d20153f7-e9ea-4c52-bd55-950dc09ab6ab/a7f345c400a48ad2c981?experience=power-bi",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Reubicación Stocks",
        "group": "COMPRAS",
        "url": "https://app.powerbi.com/groups/d44fd147-5c8a-49c9-b666-27039a11f888/reports/e9f2d751-07a6-4ff2-abf8-b6f7e03a2e17/f9cdb5f0664817712b41?experience=power-bi",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Stock y Ventas",
        "group": "COMPRAS",
        "url": "https://app.powerbi.com/groups/d44fd147-5c8a-49c9-b666-27039a11f888/reports/95f436be-a648-409c-810f-0c870de6b167/f88db8180ab398a0d214?experience=power-bi",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Vehículo Industrial AD Parts",
        "group": "COMPRAS",
        "url": "https://app.powerbi.com/groups/d44fd147-5c8a-49c9-b666-27039a11f888/reports/0a320fab-edf6-4dc4-9140-f8bb294bd6bd/ac5721623503d4cd0686?experience=power-bi",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Ventas Grupo Salas Automoción",
        "group": "ALTEC",
        "url": "https://app.powerbi.com/groups/me/reports/fde219c9-c293-4fbd-b521-1c309a7cec1b/ReportSection5692e594d1b28a09a10e?ctid=33e074aa-1197-44f3-bfc7-5634ab1dcaad&openReportSource=EmailSubscription&experience=power-bi",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Ventas Sucursales",
        "group": "DIRECCION COMERCIAL",
        "url": "https://app.powerbi.com/groups/67bbc8c4-ca83-4b3d-98d1-99109d051af0/reports/3b24f541-ca0f-4b40-b590-a58514d149b4/580e1ee68ec32a37a6fc?experience=power-bi",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Visitas",
        "group": "DIRECCION COMERCIAL",
        "url": "https://app.powerbi.com/groups/67bbc8c4-ca83-4b3d-98d1-99109d051af0/reports/1f266c9d-acbf-4ab3-8a08-f85207a63348/7515bd041929eb0ab2ed?experience=power-bi",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Visor de Tarifas",
        "group": "COMPRAS",
        "url": "https://app.powerbi.com/groups/d44fd147-5c8a-49c9-b666-27039a11f888/reports/eb0e105b-fcf4-4e4a-9d67-c617b7e3f211/ff406f18f8389418289c?experience=power-bi",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Visor Disponibilidad Trabajadores",
        "group": "RECURSOS HUMANOS",
        "url": "https://app.powerbi.com/groups/a6f47814-ba49-468b-9dd8-e08a38b2a0fb/reports/671a271e-eaa0-4665-9d59-d1ee0a84866c/f21c28871e46a80e720e?experience=power-bi",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Control de Fichajes",
        "group": "RECURSOS HUMANOS",
        "url": "https://app.powerbi.com/groups/a6f47814-ba49-468b-9dd8-e08a38b2a0fb/reports/b8c4d1d1-b6bb-4453-b126-3625e5798b3f/f21c28871e46a80e720e?experience=power-bi",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Reporte Semanal de Ausencias para RS",
        "group": "RECURSOS HUMANOS",
        "url": "https://app.powerbi.com/groups/a6f47814-ba49-468b-9dd8-e08a38b2a0fb/reports/b4f4902e-88b5-46f7-af7f-360965c6882d/d60546a7e4ddb868e008?experience=power-bi",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
]

def init_database():
    """Initialize the database with sample data if empty"""
    try:
        if reports_collection.count_documents({}) == 0:
            print("Initializing database with reports...")
            reports_collection.insert_many(reports_data)
            print(f"Inserted {len(reports_data)} reports into the database")
        else:
            print("Database already contains reports")
    except PyMongoError as e:
        print(f"Error initializing database: {e}")

# Initialize database on startup
init_database()

@app.get("/")
async def root():
    return {"message": "Power BI Directory API is running"}

@app.get("/api/reports")
async def get_reports(group: Optional[str] = None, search: Optional[str] = None):
    """Get all reports with optional filtering by group and search term"""
    try:
        # Build query
        query = {}
        if group and group != "ALL":
            query["group"] = group
        if search:
            query["name"] = {"$regex": search, "$options": "i"}
        
        # Get reports from database
        reports = list(reports_collection.find(query, {"_id": 0}))
        
        return {
            "success": True,
            "data": reports,
            "total": len(reports)
        }
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/groups")
async def get_groups():
    """Get all unique groups/areas"""
    try:
        groups = reports_collection.distinct("group")
        return {
            "success": True,
            "data": sorted(groups)
        }
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/reports/{report_id}")
async def get_report(report_id: str):
    """Get a specific report by ID"""
    try:
        report = reports_collection.find_one({"id": report_id}, {"_id": 0})
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        
        return {
            "success": True,
            "data": report
        }
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/stats")
async def get_stats():
    """Get statistics about the reports"""
    try:
        total_reports = reports_collection.count_documents({})
        
        # Count by group
        pipeline = [
            {"$group": {"_id": "$group", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        group_stats = list(reports_collection.aggregate(pipeline))
        
        return {
            "success": True,
            "data": {
                "total_reports": total_reports,
                "groups": group_stats
            }
        }
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Administration endpoints
from pydantic import BaseModel, validator

class ReportCreate(BaseModel):
    name: str
    group: str
    url: str
    
    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('El nombre del informe no puede estar vacío')
        return v.strip()
    
    @validator('group')
    def group_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('El grupo no puede estar vacío')
        return v.strip().upper()
    
    @validator('url')
    def url_must_be_powerbi(cls, v):
        if not v.strip():
            raise ValueError('La URL no puede estar vacía')
        if 'app.powerbi.com' not in v:
            raise ValueError('La URL debe ser de Power BI (app.powerbi.com)')
        return v.strip()

class ReportUpdate(BaseModel):
    name: Optional[str] = None
    group: Optional[str] = None
    url: Optional[str] = None
    
    @validator('name')
    def name_must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError('El nombre del informe no puede estar vacío')
        return v.strip() if v else v
    
    @validator('group')
    def group_must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError('El grupo no puede estar vacío')
        return v.strip().upper() if v else v
    
    @validator('url')
    def url_must_be_powerbi(cls, v):
        if v is not None:
            if not v.strip():
                raise ValueError('La URL no puede estar vacía')
            if 'app.powerbi.com' not in v:
                raise ValueError('La URL debe ser de Power BI (app.powerbi.com)')
            return v.strip()
        return v

@app.post("/api/admin/reports")
async def create_report(report: ReportCreate):
    """Create a new report"""
    try:
        # Check if report with same name and group already exists
        existing = reports_collection.find_one({"name": report.name, "group": report.group})
        if existing:
            raise HTTPException(status_code=400, detail="Ya existe un informe con ese nombre en el mismo grupo")
        
        # Create new report
        new_report = {
            "id": str(uuid.uuid4()),
            "name": report.name,
            "group": report.group,
            "url": report.url,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = reports_collection.insert_one(new_report)
        if result.inserted_id:
            # Remove MongoDB's _id from response
            new_report.pop("_id", None)
            return {
                "success": True,
                "message": "Informe creado exitosamente",
                "data": new_report
            }
        else:
            raise HTTPException(status_code=500, detail="Error al crear el informe")
            
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.put("/api/admin/reports/{report_id}")
async def update_report(report_id: str, report: ReportUpdate):
    """Update an existing report"""
    try:
        # Check if report exists
        existing = reports_collection.find_one({"id": report_id})
        if not existing:
            raise HTTPException(status_code=404, detail="Informe no encontrado")
        
        # Build update data
        update_data = {"updated_at": datetime.utcnow()}
        if report.name is not None:
            update_data["name"] = report.name
        if report.group is not None:
            update_data["group"] = report.group
        if report.url is not None:
            update_data["url"] = report.url
        
        # Check for duplicates if name or group is being updated
        if report.name is not None or report.group is not None:
            new_name = report.name if report.name is not None else existing["name"]
            new_group = report.group if report.group is not None else existing["group"]
            
            duplicate = reports_collection.find_one({
                "name": new_name, 
                "group": new_group,
                "id": {"$ne": report_id}
            })
            if duplicate:
                raise HTTPException(status_code=400, detail="Ya existe un informe con ese nombre en el mismo grupo")
        
        # Update report
        result = reports_collection.update_one({"id": report_id}, {"$set": update_data})
        
        if result.modified_count > 0:
            updated_report = reports_collection.find_one({"id": report_id}, {"_id": 0})
            return {
                "success": True,
                "message": "Informe actualizado exitosamente",
                "data": updated_report
            }
        else:
            return {
                "success": True,
                "message": "No se realizaron cambios",
                "data": existing
            }
            
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.delete("/api/admin/reports/{report_id}")
async def delete_report(report_id: str):
    """Delete a report"""
    try:
        # Check if report exists
        existing = reports_collection.find_one({"id": report_id})
        if not existing:
            raise HTTPException(status_code=404, detail="Informe no encontrado")
        
        # Delete report
        result = reports_collection.delete_one({"id": report_id})
        
        if result.deleted_count > 0:
            return {
                "success": True,
                "message": "Informe eliminado exitosamente"
            }
        else:
            raise HTTPException(status_code=500, detail="Error al eliminar el informe")
            
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/api/admin/groups")
async def create_group(group_data: dict):
    """Create a new group"""
    try:
        group_name = group_data.get("name", "").strip().upper()
        if not group_name:
            raise HTTPException(status_code=400, detail="El nombre del grupo no puede estar vacío")
        
        # Check if group already exists
        existing_groups = reports_collection.distinct("group")
        if group_name in existing_groups:
            raise HTTPException(status_code=400, detail="El grupo ya existe")
        
        return {
            "success": True,
            "message": f"Grupo '{group_name}' listo para usar",
            "data": {"name": group_name}
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.delete("/api/admin/groups/{group_name}")
async def delete_group(group_name: str):
    """Delete a group (only if it has no reports)"""
    try:
        # Check if group has reports
        reports_in_group = reports_collection.count_documents({"group": group_name})
        if reports_in_group > 0:
            raise HTTPException(
                status_code=400, 
                detail=f"No se puede eliminar el grupo '{group_name}' porque tiene {reports_in_group} informes asociados"
            )
        
        return {
            "success": True,
            "message": f"Grupo '{group_name}' eliminado exitosamente"
        }
        
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

from fastapi.staticfiles import StaticFiles
app.mount("/", StaticFiles(directory="static", html=True), name="static")