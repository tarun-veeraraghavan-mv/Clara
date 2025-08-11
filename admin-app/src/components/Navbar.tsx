import React from "react";
import Link from "next/link";

const Navbar = () => {
  return (
    <nav>
      <ul className="flex gap-3 mb-5">
        <li>
          <Link href="/">Dashboard</Link>
        </li>
        <li>Conversations</li>
        <li>
          <Link href="/bot-settings">Bot Setting</Link>
        </li>
        <li>
          <Link href="/analytics">Analytics</Link>``
        </li>
        <li>User Feedback</li>
      </ul>
    </nav>
  );
};

export default Navbar;
