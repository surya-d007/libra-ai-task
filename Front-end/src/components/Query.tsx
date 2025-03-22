import React, { useState } from "react";

interface Match {
  name: string;
  id: string;
  downloadLink: string;
  score: number;
}

const Query = () => {
  const [query, setQuery] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const [results, setResults] = useState<{
    matches: Match[];
    answer: string;
  } | null>(null);

  const handleSubmit = async () => {
    if (!query.trim()) {
      alert("Please enter a query.");
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(
        `http://localhost:8000/search?query=${encodeURIComponent(query)}`,
        {
          method: "POST",
          headers: {
            Accept: "application/json",
          },
        }
      );

      if (response.ok) {
        const data = await response.json();
        console.log("Search Results:", data);
        setResults(data);
      } else {
        console.error("API Error:", await response.text());
      }
    } catch (error) {
      console.error("Error during API call:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-6">
      <div className="p-6 bg-white rounded shadow-md w-full max-w-md">
        <h1 className="text-2xl font-bold mb-4">Search Your Files</h1>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter your query..."
          className="w-full p-2 border border-gray-300 rounded mb-4"
        />
        <button
          onClick={handleSubmit}
          disabled={loading}
          className="w-full p-2 bg-blue-500 text-white rounded hover:bg-blue-700 disabled:bg-gray-400"
        >
          {loading ? "Searching..." : "Search"}
        </button>

        {loading && (
          <p className="text-blue-500 mt-4">Loading results, please wait...</p>
        )}

        {/* Show Results */}
        {results && (
          <div className="mt-6">
            <h2 className="text-lg font-semibold mb-2">Search Results</h2>
            {results.matches.length > 0 ? (
              <ul className="mb-4">
                {results.matches.map((match, index) => (
                  <li key={index} className="mb-2">
                    <span className="font-medium">{match.name}</span> -{" "}
                    <a
                      href={match.downloadLink}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-500 hover:underline"
                    >
                      Download
                    </a>
                  </li>
                ))}
              </ul>
            ) : (
              <p>No matching files found.</p>
            )}

            <h3 className="text-lg font-medium mt-4">Answer:</h3>
            <p className="text-gray-700">{results.answer}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Query;
