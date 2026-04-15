flowchart TD
    A([User Preferences\ngenre · mood · energy · valence · danceability · acousticness])
    A --> B[Load all 20 songs from songs.csv]
    B --> C{For each song}

    C --> D[genre_score = 3.0 if match else 0.0]
    C --> E[mood_score = 2.0 if match else 0.0]
    C --> F[energy_score = 1.0 - abs song - target]
    C --> G[valence_score = 1.0 - abs song - target]
    C --> H[danceability_score = 1.0 - abs song - target]
    C --> I[acousticness_score = 1.0 - abs song - target]

    D & E & F & G & H & I --> J[total_score = sum of all six\nmax 9.0 pts]

    J --> K{More songs?}
    K -- Yes --> C
    K -- No --> L[Sort all songs highest to lowest score]
    L --> M([Return Top K Recommendations])