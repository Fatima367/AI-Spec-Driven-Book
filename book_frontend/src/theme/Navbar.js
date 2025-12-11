import React from 'react';
import OriginalNavbar from '@theme-original/Navbar';

// Since wrapping caused issues, we'll use a CSS approach to hide/show auth elements
// The NavbarAuth component will be added separately in a custom layout or through a different approach

export default function Navbar(props) {
  return <OriginalNavbar {...props} />;
}