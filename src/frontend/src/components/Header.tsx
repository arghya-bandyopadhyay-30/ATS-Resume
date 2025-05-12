// components/Header.tsx
import React from 'react';
import { NavLink } from 'react-router-dom';
import '../index.css';
import twLogo from '../assets/thoughtworks.png';

export const Header: React.FC = () => (
  <header>
    <div className="bg-dark-blue h-16 flex items-center justify-between px-4">
      <div className="flex items-center">
        <img src={twLogo} alt="Thoughtworks" className="h-8 w-auto mr-3" />
        <span className="mx-2 text-white">|</span>
        <span className="text-white font-semibold text-lg">ASAP - AST</span>
      </div>
      <div className="flex space-x-4">
        <NavLink
          to="/"
          className={({ isActive }) =>
            `text-sm text-white px-3 py-1 rounded-md hover:bg-sapphire ${
              isActive ? 'bg-sapphire' : ''
            }`
          }
        >
          Home
        </NavLink>
        <NavLink
          to="/reminder"
          className={({ isActive }) =>
            `text-sm text-white px-3 py-1 rounded-md hover:bg-sapphire ${
              isActive ? 'bg-sapphire' : ''
            }`
          }
        >
          Resume Update Notifier
        </NavLink>
        <NavLink
          to="/rank"
          className={({ isActive }) =>
            `text-sm text-white px-3 py-1 rounded-md hover:bg-sapphire ${
              isActive ? 'bg-sapphire' : ''
            }`
          }
        >
          Staffing Assistant
        </NavLink>
      </div>
    </div>
  </header>
);
