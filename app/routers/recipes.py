from typing import Literal

from fastapi import APIRouter, HTTPException, Response, status

from app.schemas import Category, Recipe, RecipeCreate, RecipeUpdate

router = APIRouter(prefix="/recipes", tags=["recipes"])

_recipes: dict[int, Recipe] = {}
_next_id = 1


def reset_store() -> None:
    global _next_id
    _recipes.clear()
    _next_id = 1


def _get_or_404(recipe_id: int) -> Recipe:
    recipe = _recipes.get(recipe_id)
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@router.post("", response_model=Recipe, status_code=status.HTTP_201_CREATED)
def create_recipe(payload: RecipeCreate) -> Recipe:
    global _next_id
    recipe = Recipe(id=_next_id, **payload.model_dump())
    _recipes[recipe.id] = recipe
    _next_id += 1
    return recipe


@router.get("", response_model=list[Recipe])
def list_recipes(
    category: Category | None = None,
    sort_by: Literal["cook_time"] | None = None,
    order: Literal["asc", "desc"] = "asc",
) -> list[Recipe]:
    recipes = list(_recipes.values())
    if category is not None:
        recipes = [r for r in recipes if r.category == category]
    if sort_by == "cook_time":
        # 조리 시간이 없는 레시피는 정렬 방향과 상관없이 맨 뒤에 둔다.
        timed = [r for r in recipes if r.cook_time_minutes is not None]
        untimed = [r for r in recipes if r.cook_time_minutes is None]
        timed.sort(key=lambda r: r.cook_time_minutes, reverse=order == "desc")
        recipes = timed + untimed
    return recipes


@router.get("/{recipe_id}", response_model=Recipe)
def get_recipe(recipe_id: int) -> Recipe:
    return _get_or_404(recipe_id)


@router.put("/{recipe_id}", response_model=Recipe)
def update_recipe(recipe_id: int, payload: RecipeUpdate) -> Recipe:
    recipe = _get_or_404(recipe_id)
    updated = recipe.model_copy(update=payload.model_dump(exclude_unset=True))
    _recipes[recipe_id] = updated
    return updated


@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe(recipe_id: int) -> Response:
    _get_or_404(recipe_id)
    del _recipes[recipe_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)
