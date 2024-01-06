import Link from "next/link"
import React from "react"

export default async function Page() {
    /**************************************************************************/
    /* Render */
    return (
        <div className="p-2">
            <h1 className="text-4xl">What is Flotion?</h1>

            <p className="mt-2">
                Flotion (<b>Fl</b>etcher&apos;s N<b>otion</b>) is my take on a collaborative, real-time document editor.
            </p>

            <h2 className="mt-8 text-2xl">Philosophy</h2>

            <p className="mt-2">
                This project was (partially) inspired by{" "}
                <Link
                    href="https://simonwillison.net/"
                    target="_blank"
                >
                    Simon Willison&apos;s
                </Link>{" "}
                <Link
                    href="https://datasette.io/"
                    target="_blank"
                >
                    Datasette
                </Link>
                . With Datasette, you own all of your data, you simply use the tool to explore and work with that data.
                Your data shouldn&apos;t be locked-down to the tool.
            </p>

            <h2 className="mt-8 text-2xl">Key Features</h2>

            <h3 className="mt-4 text-xl">No custom account creation or management</h3>

            <p className="mt-2">Sign-in with Google and you&apos;re good to go.</p>

            <h3 className="mt-4 text-xl">You own your data</h3>

            <p className="mt-2">
                I will never be able to view your documents without your explicit permission. All documents are stored
                in Google Drive, and access is granted through Google Drive permissions.
            </p>

            <h3 className="mt-4 text-xl">Markdown friendly</h3>

            <p className="mt-2">Import your existing markdown files as-is.</p>

            <h3 className="mt-4 text-xl">Realtime collaboration</h3>

            <p className="mt-2">
                View, comment, and edit shared documents with others in a realtime, collaborative manner.
            </p>
        </div>
    )
}
