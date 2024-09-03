import { Inter } from 'next/font/google';
import { Lusitana } from 'next/font/google';
import { Space_Grotesk } from 'next/font/google';
import { IBM_Plex_Mono } from 'next/font/google';
 
export const inter = Inter({ subsets: ['latin'] });
export const lusitana = Lusitana({weight: ["400", "700"], subsets: ['latin']});
export const spaceGrotesk = Space_Grotesk({weight: ["500", "600", "700"], subsets: ['latin'], style: ["normal"]});
export const ibmPlexMono = IBM_Plex_Mono({weight: ["400", "500", "600", "700"], subsets: ['latin'], style: ["normal", "italic"]});
