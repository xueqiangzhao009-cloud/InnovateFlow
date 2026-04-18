import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './global.css'
import Application from './Application.tsx';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Application />
  </StrictMode>,
)
