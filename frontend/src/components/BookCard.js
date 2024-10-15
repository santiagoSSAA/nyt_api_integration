import React from 'react';
import '../styles/BookCard.css';

const BookCard = ({ book }) => {
    return (
        <div className="book-card">
            <img src={book.book_image} alt={book.title} className="book-image" />
            <h2 className="book-title">{book.title}</h2>
            <h3 className="book-author">{book.author}</h3>
            <p className="book-description">{book.description}</p>
            <div className="buy-links">
                {book.buy_links.map((link, index) => (
                    <a key={index} href={link.url} target="_blank" rel="noopener noreferrer" className="buy-link">
                        {link.name}
                    </a>
                ))}
            </div>
        </div>
    );
};

export default BookCard;
