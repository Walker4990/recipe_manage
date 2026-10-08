from pydantic import BaseModel, Field


class RecipeBase(BaseModel):
    title: str = Field(min_length=1)
    description: str | None = None
    ingredients: list[str] = []
    steps: list[str] = []
    cook_time_minutes: int | None = Field(default=None, ge=0)


class RecipeCreate(RecipeBase):
    pass


class RecipeUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1)
    description: str | None = None
    ingredients: list[str] | None = None
    steps: list[str] | None = None
    cook_time_minutes: int | None = Field(default=None, ge=0)


class Recipe(RecipeBase):
    id: int
