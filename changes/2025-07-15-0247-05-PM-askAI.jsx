import React, { useState } from 'react';
import '@fortawesome/fontawesome-free/css/all.min.css';
import { History } from './history';


export default function AskAI({ inputText, setInputText, onSubmit }) {
    const [sidebarOpen, setSidebarOpen] = useState(false);


    const toggleSidebar = () => {
        setSidebarOpen(!sidebarOpen);
    };

    const handleKeyDown = (e) => {
        if (e.key === "Enter" && inputText.trim()) {
            onSubmit(inputText);
        }
    };


    return (
        <div className="ask-ai-container">
            {/* Sidebar */}
            <History sidebarOpen={sidebarOpen} toggleSidebar={toggleSidebar} />


            {/* Main Content */}
            <div className={`main-content ${sidebarOpen ? 'shifted' : ''}`}>
                {!sidebarOpen && (
                    <button className="menu-toggle" onClick={toggleSidebar}>
                        <i className="fas fa-bars" style={{ color: '#ffffff' }}></i>
                    </button>
                )}


                <div className='question-section'>
                    <h1>How can I assist you to prove your point?</h1>
                    <div className='question-box'>
                        <i className="fa-solid fa-magnifying-glass" style={{ color: '#8f9194', marginRight: '0.5rem' }}></i>
                        <input
                            type="text"
                            placeholder="Ask a question"
                            value={inputText}
                            onChange={(e) => setInputText(e.target.value)}
                            onKeyDown={handleKeyDown}
                        />
                    </div>
                    <p>Powered by AI, answers are based on published research papers.</p>

                    {/* <div className='parent-sample-search'>
... (truncated for brevity)