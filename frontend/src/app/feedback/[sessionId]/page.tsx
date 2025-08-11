"use client";

import { analyzeCustomerFeedback } from "@/services/ai";
import { useParams, useRouter } from "next/navigation";
import { useState } from "react";
import { FaRegStar } from "react-icons/fa";
import { FaStar } from "react-icons/fa";

export default function Page() {
  const params = useParams<{ sessionId: string }>();
  const router = useRouter();

  const [rating, setRating] = useState(0);
  const [review, setReview] = useState("");

  async function handleSubmit() {
    if (!rating || !review) {
      return;
    }

    await analyzeCustomerFeedback(rating, review, 1, Number(params.sessionId));

    router.push("/");
  }

  return (
    <div className="absolute top-[45%] left-[50%] w-[600px] translate-x-[-50%] translate-y-[-50%] bg-gray-100 px-3 py-6 rounded-lg shadow-xl">
      <p className="font-bold text-2xl text-center mb-5">
        Rate the customer support
      </p>

      <ul className="flex gap-3 justify-center mb-4">
        {[1, 2, 3, 4, 5].map((s, index) => (
          <li key={index} onClick={() => setRating(index + 1)}>
            {index < rating ? (
              <FaStar size={25} fill="gold" />
            ) : (
              <FaRegStar size={25} fill="gold" />
            )}
          </li>
        ))}
      </ul>

      <div className="mb-4">
        <label className="mb-3 block">
          Why did you like or dislike the conversation? Any specific examples on
          where to improve the customer agent
        </label>
        <textarea
          className="bg-gray-200 w-[100%] rounded-md outline-none p-2 h-[150px] block"
          value={review}
          onChange={(e) => setReview(e.target.value)}
        />
      </div>
      <div>
        <button
          className="px-3 py-1 bg-blue-400 hover:bg-blue-500 rounded-full cursor-pointer"
          onClick={handleSubmit}
        >
          Submit your response
        </button>
      </div>
    </div>
  );
}
