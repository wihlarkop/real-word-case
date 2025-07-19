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
    return f"""Create a realistic work scenario for a {role} in {industry} (difficulty: {difficulty}).
        Write 3-4 sentences describing a product or technical challenge that needs to be solved. Write it as if a product manager or stakeholder is explaining the problem to you.
        
        Do not include:
        - Code examples or technical implementation details
        - Bullet points or structured lists
        - Headers or markdown formatting
        - The words "title", "industry", "role", or "difficulty"
        
        Just write a plain narrative describing what needs to be built or solved.
        
        Example format: "The customer service team is struggling with... They need a solution that can... The goal is to..."
        
        Generate the scenario now:
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
