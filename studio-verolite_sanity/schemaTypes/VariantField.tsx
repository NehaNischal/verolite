import React from 'react'
import { FieldProps, useFormValue } from 'sanity'

export interface VariantHeaders {
  col1?: string
  col2?: string
  col3?: string
  col4?: string
  col5?: string
  col6?: string
}

/**
 * Creates a Sanity Field Component that dynamically reads the product's
 * `variantHeaders` configuration to change the field title in the Studio UI,
 * or hide the field if the header is cleared or set to '-'.
 */
export function createVariantFieldComponent(
  colKey: keyof VariantHeaders,
  defaultTitle: string
) {
  return function DynamicVariantField(props: FieldProps) {
    const variantHeaders = useFormValue(['variantHeaders']) as VariantHeaders | undefined
    const customHeader = variantHeaders?.[colKey]

    // If the user intentionally cleared this header or set it to '-', hide the field in the variant form
    if (customHeader !== undefined && (customHeader.trim() === '' || customHeader.trim() === '-')) {
      return null
    }

    const displayTitle = customHeader?.trim() || defaultTitle

    return props.renderDefault({
      ...props,
      title: displayTitle,
      description: customHeader?.trim()
        ? `Configured column title: "${displayTitle}"`
        : `Default: ${defaultTitle} (Set in "Variant Table Columns & Headers" above)`,
    })
  }
}
