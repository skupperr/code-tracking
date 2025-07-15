import { useEffect, useState, useRef } from "react";
import { useLocation } from "react-router-dom";
import { useApi } from "../utils/api";
import { useAuth } from "@clerk/clerk-react";


export default function QuestionAnswer() {
    const { userId } = useAuth();
    const location = useLocation();
    const { docId } = location.state || {};
    const { makeRequest } = useApi();

    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const textareaRef = useRef(null); // 👈 Add textarea ref

    useEffect(() => {
        const fetchEntry = async () => {
            if (!userId || !docId) return;
            try {
                const res = await makeRequest(`user-history/${docId}`);
                if (res.status === "success") {
                    setData(res.data);
                } else {
                    console.warn("Entry not found");
                }
            } catch (err) {
                console.error("Failed to fetch entry:", err);
            } finally {
                setLoading(false);
            }
        };



        fetchEntry();
    }, [userId, docId]);

    useEffect(() => {
        if (textareaRef.current) {
            textareaRef.current.style.height = "auto";
            textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
        }
    }, [data]);

    if (loading)
        return (
            <div className="status-message loading">
                <p>🧠 Loading...</p>
            </div>
... (truncated for brevity)