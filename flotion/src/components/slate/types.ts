import { BaseEditor } from "slate"
import { ReactEditor } from "slate-react"

/******************************************************************************/
/* Custom text types */
export interface PlainText {
    type: "plain"
    text: string
}

export interface CodeText {
    type: "code"
    text: string
}

export interface FormattedText {
    type: "formatted"
    text: string
    bold?: boolean
    italics?: boolean
    strikethrough?: boolean
}

export interface LinkText {
    type: "link"
    text: string
    link: string
    bold?: boolean
    italics?: boolean
    strikethrough?: boolean
}

export interface ImageText {
    type: "image"
    altText: string
    link: string
}

type CustomText = PlainText | CodeText | FormattedText | LinkText | ImageText

/******************************************************************************/
/* Custom element types */
export interface HeaderElement {
    type: "header"
    level: 1 | 2 | 3
    children: Array<PlainText>
}

export interface ParagraphElement {
    type: "paragraph"
    children: Array<CustomText>
}

export interface ListElement {
    type: "list"
    ordered: boolean
    children: Array<CustomElement>
}

export interface CodeElement {
    type: "code"
    language: string
    children: Array<PlainText>
}

export interface BlockquoteElement {
    type: "blockquote"
    children: Array<CustomElement>
}

export interface DividerElement {
    type: "divider"
}

export type CustomElement =
    | HeaderElement
    | ParagraphElement
    | ListElement
    | CodeElement
    | BlockquoteElement
    | DividerElement

/******************************************************************************/
/* Module */
declare module "slate" {
    interface CustomTypes {
        Editor: BaseEditor & ReactEditor
        Element: CustomElement
        Text: CustomText
    }
}
