import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const Auth = () => {
  const [authUrl, setAuthUrl] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchAuthUrl = async () => {
      try {
        const response = await fetch("http://localhost:8000/auth-url");
        const data = await response.json();
        setAuthUrl(data.auth_url);
      } catch (error) {
        console.error("Error fetching auth URL:", error);
      }
    };

    fetchAuthUrl();
  }, []);

  // Mock API response for testing
  const mockSaveUserData = () => {
    navigate("/home"); // Navigate to home
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      {authUrl ? (
        <a
          href={authUrl}
          className="px-4 py-2 font-semibold text-white bg-blue-500 rounded hover:bg-blue-700"
          onClick={mockSaveUserData}
        >
          Authenticate with Google
        </a>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default Auth;
