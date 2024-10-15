import React, { Component } from 'react';
import './styles/style.css'; // Asegúrate de que la ruta sea correcta
import GenreSelector from './components/GenreSelector';
import BestSellersCarousel from './components/BestSellersCarousel';
import LoadingIndicator from './components/LoadingIndicator';

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            genres: [],
            bestSellers: [], // Inicializa como un array vacío
            loading: true,
        };
    }

    async componentDidMount() {
        this.loadGenres();  // Cargar géneros al inicio
        this.interval = setInterval(this.loadGenres, 15000);
    }
    
    componentWillUnmount() {
        clearInterval(this.interval);  // Limpiar intervalo al desmontar
    }

    loadGenres = async () => {
        try {
            const response = await fetch('http://localhost:8000/api/books/genres');
            const data = await response.json();
            this.setState({ genres: data.content, loading: false });
        } catch (error) {
            console.error('Error al cargar géneros:', error);
            this.setState({ loading: false });
        }
    };

    handleGenreChange = async (selectedGenre) => {
        const formattedGenre = selectedGenre.trim().replace(/\s+/g, '_');
        this.setState({ loading: true });
        try {
            console.log(`${selectedGenre} ${formattedGenre}`);
            const response = await fetch(`http://localhost:8000/api/books/${formattedGenre}/best-sellers`);
            const data = await response.json();
            this.setState({ bestSellers: data.books, loading: false });
        } catch (error) {
            console.error('Error al cargar best sellers:', error);
            this.setState({ loading: false });
        }
    };

    render() {
        const { genres, bestSellers, loading } = this.state;

        return (
            <div className="App">
                {loading ? (
                    <LoadingIndicator />
                ) : (
                    <div>
                        <GenreSelector genres={genres} onGenreChange={this.handleGenreChange} />
                        {bestSellers && bestSellers.length > 0 && ( // Verificar si hay best sellers antes de renderizar el carrusel
                            <BestSellersCarousel books={bestSellers} />
                        )}
                    </div>
                )}
            </div>
        );
    }
}

export default App;
