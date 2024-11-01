import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

const content = '<h3>WINGSプロジェクト</h3> <img src="https://wings.msn.to/image/wings.jpg" />';
const dest = 'http://ja.react.dev'
const attrs = {
  href: 'https://wings.msn.to/',
  download: false,
  target: '_blank',
  rel: 'help',
};
const props = {
  color: 'White',
  backgroundColor: 'Blue',
  padding: 3
};

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <p style={props}>WINGSプロジェクト</p>
    <div dangerouslySetInnerHTML={{ __html: content }} />
    <div>{'Tom &amp; Jerry'}</div>
    <a href={attrs.href} download={attrs.download} target={attrs.target} rel={attrs.rel}>サポートページ</a>
    <a {...attrs}>サポートページ</a>
  </StrictMode>,
)
