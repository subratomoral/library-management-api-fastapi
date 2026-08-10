from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
from typing import Optional

app = FastAPI()


class Book(BaseModel):
    title: str = Field(
        min_length=3, max_length=50, description="Enter Title:", examples=["titanic"]
    )
    author: str = Field(
        min_length=3,
        max_length=50,
        description="Enter Author Name",
        examples=["James clear"],
    )
    price: float = Field(gt=0, lt=100000, description="Enter price", examples=[499.99])


class ReplaceBook(BaseModel):
    title: str = Field(
        min_length=3, max_length=50, description="Enter Title:", examples=["titanic"]
    )
    author: str = Field(
        min_length=3,
        max_length=50,
        description="Enter Author Name",
        examples=["James clear"],
    )
    price: float = Field(gt=0, lt=100000, description="Enter price", examples=[499.99])


class UpdateBook(BaseModel):
    author: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=50,
        description="Enter Title",
        examples=["titanic"],
    )
    price: Optional[float] = Field(
        default=None, gt=0, description="Enter Price", examples=[500.00]
    )


library: list[Book] = []


@app.post("/book", response_model=Book, tags=["Library"])
def post_book(books: Book):
    for b in library:
        if b.title == books.title:
            raise HTTPException(status_code=409, detail="Book exists Already")
    library.append(books)
    return books


@app.patch("/update_library", response_model=Book, tags=["Library"])
def update_lib(title: str, books: UpdateBook):
    for book in library:
        if book.title.strip().lower() == title.strip().lower():
            if books.author is not None:
                book.author = books.author
            if books.price is not None:
                book.price = books.price
            return book
    raise HTTPException(status_code=404, detail="title not found")


@app.get("/library", response_model=list[Book], tags=["Library"])
def get_books():
    return library


@app.get("/library/get_by_title/{title}", response_model=Book, tags=["Library"])
def get_by_title(title: str):
    for book in library:
        if book.title.strip().lower() == title.strip().lower():
            return book
    raise HTTPException(status_code=404, detail="book not found")


@app.put("/Update_library", response_model=Book, tags=["Library"])
def update_book(title: str, books: ReplaceBook):
    for book in library:
        if book.title.strip().lower() == title.strip().lower():
            for b in library:
                if (
                    b.title.strip().lower() == books.title.strip().lower()
                    and b is not book
                ):
                    raise HTTPException(
                        status_code=409, detail="book title already exists"
                    )

            book.title = books.title
            book.author = books.author
            book.price = books.price
            return book
    raise HTTPException(status_code=404, detail="book not found")


@app.delete("/deleteBook", tags=["Library"])
def delete_library(title: str):
    for book in library:
        if book.title.strip().lower() == title.strip().lower():
            library.remove(book)
            return {"status": "book remove successfully"}

    raise HTTPException(status_code=404, detail="book not found")
