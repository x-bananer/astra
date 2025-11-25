import { NextResponse } from "next/server";

export function middleware(req) {
	const url = req.nextUrl.clone();
	const path = url.pathname;

	const token = req.cookies.get("astra.access_token")?.value;

	if (
		path.startsWith("/images") ||
		path.startsWith("/img") ||
		path.startsWith("/assets") ||
		path.startsWith("/icons") ||
		path.endsWith(".png") ||
		path.endsWith(".jpg") ||
		path.endsWith(".jpeg") ||
		path.endsWith(".svg") ||
		path.endsWith(".webp") ||
		path === "/favicon.ico"
	) {
		return NextResponse.next();
	}

	if (path.includes("login")) {
		if (token) {
			url.pathname = "/";
			return NextResponse.redirect(url);
		}
		return NextResponse.next();
	}

	if (!token) {
		url.pathname = "/login";
		return NextResponse.redirect(url);
	}

	return NextResponse.next();
}

export const config = {
	matcher: [
		"/((?!_next).*)"
	],
};