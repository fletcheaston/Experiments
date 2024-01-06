"use client"

import { zodResolver } from "@hookform/resolvers/zod"
import React, { useCallback, useMemo } from "react"
import { useForm } from "react-hook-form"
import * as z from "zod"

import { CustomEditor } from "@components/slate/custom-editor"
import { Button } from "@components/ui/button"
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@components/ui/form"
import { Input } from "@components/ui/input"

import { UpdateIcon } from "@icons/update"

const formSchema = z.object({
    title: z.string().min(8, "Title must contain at least 8 characters."),
    content: z.string().min(1, "Content cannot be empty."),
})
type FormSchema = z.infer<typeof formSchema>

export default function Page() {
    /**************************************************************************/
    /* State */
    const form = useForm<FormSchema>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            title: "",
            content: "",
        },
    })

    const isSubmitting = useMemo(() => {
        return form.formState.isSubmitting
    }, [form])

    const isDirty = useMemo(() => {
        return form.formState.isDirty
    }, [form])

    const saveButton: React.JSX.Element = useMemo(() => {
        if (isSubmitting) {
            return (
                <Button
                    type="submit"
                    className="mt-6 flex gap-x-2 text-lg"
                    disabled
                >
                    <UpdateIcon className="animate-spin" />
                    Saving
                </Button>
            )
        }

        if (isDirty) {
            return (
                <Button
                    type="submit"
                    className="mt-6 flex gap-x-2 text-lg"
                >
                    Save
                </Button>
            )
        }

        return (
            <Button
                type="submit"
                className="mt-6 flex gap-x-2 text-lg"
                disabled
            >
                Save
            </Button>
        )
    }, [isSubmitting, isDirty])

    /**************************************************************************/
    /* Callbacks */
    const onSubmit = useCallback(
        (values: FormSchema) => {
            console.log(values)
            form.reset(values)
        },
        [form],
    )

    /**************************************************************************/
    /* Render */
    return (
        <div className="p-2">
            <Form {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)}>
                    <div className="flex justify-between">
                        <FormField
                            control={form.control}
                            name="title"
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel>Title</FormLabel>
                                    <FormControl>
                                        <Input
                                            placeholder="Untitled"
                                            className="w-fit min-w-[400px] text-4xl"
                                            {...field}
                                        />
                                    </FormControl>
                                    <FormMessage />
                                </FormItem>
                            )}
                        />

                        {saveButton}
                    </div>

                    <div className="mt-2">
                        <CustomEditor />
                    </div>
                </form>
            </Form>
        </div>
    )
}
