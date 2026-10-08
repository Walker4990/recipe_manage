from enum import Enum

from pydantic import BaseModel, Field


class Category(str, Enum):
    KOREAN = "한식"
    WESTERN = "양식"
    CHINESE = "중식"
    OTHER = "기타"


class RecipeBase(BaseModel):
    title: str = Field(min_length=1)
    description: str | None = None
    ingredients: list[str] = []
    steps: list[str] = []
    cook_time_minutes: int | None = Field(default=None, ge=0)
    category: Category = Category.OTHER


class RecipeCreate(RecipeBase):
    pass


class RecipeUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1)
    description: str | None = None
    ingredients: list[str] | None = None
    steps: list[str] | None = None
    cook_time_minutes: int | None = Field(default=None, ge=0)
    category: Category | None = None


class Recipe(RecipeBase):
    id: int
