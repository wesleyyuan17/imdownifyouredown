import React from 'react';
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import './App.css';

import { HomePage } from "./components/HomePage";
import { HeaderBanner, User, Event } from "./components/util";
import { EventPage } from './components/EventPage';

const App: React.FC = () => {
  const user: User = { user_id: 1, username: "User" };
  const event: Event = {
    event_id: 1,
    name: "TestEvent",
    users: [user, user],
    description: "This is a test event"
  }
  return (
    <Router>
      <div>
        {/* Render the HeaderBanner component on every page */}
        <header><HeaderBanner user={user} /></header>

        {/* Use Routes to render only the first matching Route */}
        <Routes>
          <Route path="/home" element={<HomePage />} />
          <Route path="/events" element={<EventPage user={user} event={event} />} />
          {/* <Route path="/user" component={UserPage} /> */}

          {/* Redirect to the home page if no route matches */}
          <Route path="*" element={<HomePage />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
