import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from ollama import chat, ChatResponse
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from starlette.middleware.cors import CORSMiddleware


class Settings(BaseSettings):
    APP_NAME: str = "RealWorldCase API"
    APP_VERSION: str = "0.0.1"
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    DEBUG: bool = True


class CategorySchema(BaseModel):
    value: str
    label: str


settings = Settings()

industries: list[CategorySchema] = [
    CategorySchema(value="any_industries", label="Any Industries"),
    CategorySchema(value="fintech", label="Fintech"),
    CategorySchema(value="ecommerce", label="E-commerce"),
    CategorySchema(value="healthcare", label="Healthcare"),
    CategorySchema(value="edutech", label="Edutech"),
    CategorySchema(value="banking", label="Banking"),
    CategorySchema(value="gaming", label="Gaming"),
    CategorySchema(value="media", label="Media"),
    CategorySchema(value="logistics", label="Logistics"),
    CategorySchema(value="travel", label="Travel"),
    CategorySchema(value="saas", label="SaaS"),
    CategorySchema(value="real_estate", label="Real Estate"),
    CategorySchema(value="govtech", label="Govtech"),
]

difficulties: list[CategorySchema] = [
    CategorySchema(value="any_difficulty", label="Any Difficulty"),
    CategorySchema(value="easy", label="Easy"),
    CategorySchema(value="medium", label="medium"),
    CategorySchema(value="hard", label="Hard")
]

roles: list[CategorySchema] = [
    CategorySchema(value="any_role", label="Any Role"),
    CategorySchema(value="frontend_engineer", label="Frontend Engineer"),
    CategorySchema(value="backend_engineer", label="Backend Engineer"),
    CategorySchema(value="fullstack_engineer", label="Fullstack Engineer"),
    CategorySchema(value="mobile_engineer", label="Mobile Engineer"),
    CategorySchema(value="ai_engineer", label="AI Engineer"),
]


class HealthResponse(BaseModel):
    name: str
    version: str


class ChallengeRequest(BaseModel):
    industry: str
    role: str
    difficulty: str


def build_prompt(industry: str, role: str, difficulty: str) -> str:
    return f"""
    You are a scenario designer generating creative, open-ended prompts for software engineers.
    
    Generate a short, realistic product or stakeholder request as a markdown-formatted narrative.
    
    Context:
    - Role: {role} software engineer
    - Industry: {industry}
    - Difficulty level: {difficulty}
    
    Guidelines:
    - Use 3–5 sentences in total
    - Present a concise product need or situation without introducing sample data, code, or structure
    - Write in natural, narrative form – like a product brief or real-world stakeholder request
    - Avoid bullet points, headers, code blocks, and JSON
    - Do not mention "title", "industry", or any other metadata
    - The challenge should inspire creative engineering thought without being too long or too prescriptive
    
    Only return the markdown description as a plain string.
    """


def run(prompt: str) -> str:
    response: ChatResponse = chat(
        model='gemma3:4b',
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.message.content


app = FastAPI(default_response_class=ORJSONResponse)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def health():
    return HealthResponse(
        name=settings.APP_NAME,
        version=settings.APP_VERSION,
    )


@app.get("/api/v1/category")
async def get_category_list() -> dict[str, list[CategorySchema]]:
    return {
        "industries": industries,
        "difficulties": difficulties,
        "roles": roles,
    }


@app.post("/api/v1/challenge")
async def get_challenge(payload: ChallengeRequest) -> dict[str, str]:
    if payload.industry not in {item.value for item in industries}:
        return {"error": "Invalid industry"}
    if payload.role not in {item.value for item in roles}:
        return {"error": "Invalid role"}
    if payload.difficulty not in {item.value for item in difficulties}:
        return {"error": "Invalid difficulty"}

    prompt = build_prompt(industry=payload.industry, role=payload.role, difficulty=payload.difficulty)
    result = run(prompt)

    return {
        "result": result
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
