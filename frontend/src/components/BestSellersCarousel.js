import React from 'react';
import Slider from 'react-slick'; // Importar el componente Slider
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';
import '../styles/BestSellersCarousel.css';

const BestSellersCarousel = ({ books }) => {
    const settings = {
        dots: true,
        infinite: true,
        speed: 500,
        slidesToShow: 3,
        slidesToScroll: 1,
        arrows: true,
        responsive: [
            {
                breakpoint: 1024,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 1,
                    dots: true,
                    arrows: true,
                },
            },
            {
                breakpoint: 600,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1,
                    arrows: true,
                },
            },
        ],
    };

    return (
        <div>
            <h2>Best Sellers</h2>
            <Slider {...settings}>
                {books.map((book, index) => (
                    <div key={index} style={{ padding: '10px' }}>
                        <img 
                            src={book.book_image} 
                            alt={book.title} 
                            style={{ width: '100%', borderRadius: '8px' }} 
                        />
                        <h3>{book.title}</h3>
                        <p><strong>Author:</strong> {book.author}</p>
                        <p><strong>Rank:</strong> {book.rank}</p>
                        <p>{book.description}</p>
                        <a 
                            href={book.amazon_product_url} 
                            target="_blank" 
                            rel="noopener noreferrer"
                            className="amazon-button"
                        >
                            Buy on Amazon
                        </a>
                    </div>
                ))}
            </Slider>
        </div>
    );
};

export default BestSellersCarousel;
