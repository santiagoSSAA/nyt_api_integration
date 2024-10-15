import React from 'react';
import '../styles/GenreSelector.css';

const GenreSelector = ({ genres, onGenreChange }) => {
    return (
        <div>
            <h2>Selecciona un Género</h2>
            {genres && genres.length > 0 ? (
                <div className='genre-selector'>
                    <select onChange={(e) => onGenreChange(e.target.value)}>
                        <option value="">Seleccionar Genero</option>
                        {genres.map((genre, index) => (
                            <option key={index} value={genre.replace(" ", "_")}>
                                {genre}
                            </option>
                        ))}
                    </select>
                </div>
            ) : (
                <p>Cargando géneros...</p>
            )}
        </div>
    );
};

export default GenreSelector;
