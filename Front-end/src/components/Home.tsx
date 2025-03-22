import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

const Home = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [code, setCode] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Extract 'code' from URL
    const params = new URLSearchParams(location.search);
    const authCode = params.get("code");

    if (authCode) {
      setCode(authCode);
      localStorage.setItem("authCode", authCode);
      console.log("Authorization code saved to localStorage:", authCode);
      sendAuthCodeToAPI(authCode);
    } else {
      const storedCode = localStorage.getItem("authCode");
      if (storedCode) {
        setCode(storedCode);
        sendAuthCodeToAPI(storedCode);
      } else {
        console.log("No authorization code found.");
      }
    }
  }, [location.search]);

  const sendAuthCodeToAPI = async (authCode: string) => {
    setLoading(true);
    try {
      const response = await fetch(
        `http://localhost:8000/ingest?auth_code=${authCode}`,
        {
          method: "POST",
          headers: {
            Accept: "application/json",
          },
        }
      );

      if (response.ok) {
        console.log("API Response: Successfully ingested files.");
        navigate("/query"); // Navigate to query on success
      } else {
        const errorData = await response.json();
        console.error("API Error:", errorData);
      }
    } catch (error) {
      console.error("Error during API call:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      {loading ? (
        <div className="flex flex-col items-center">
          <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
          <p className="text-lg text-blue-500 mt-4">
            Ingesting files... Please wait.
          </p>
        </div>
      ) : code ? (
        <p className="text-lg text-green-600">Authorization Code: {code}</p>
      ) : (
        <p className="text-lg text-red-600">No Authorization Code Found</p>
      )}
    </div>
  );
};

export default Home;
