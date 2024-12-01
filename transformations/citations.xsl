<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <!--  word lists -->
    <xsl:variable name="positive-words" select="'evidence, growing evidence, included, evaluated, validated, using, add, correlation associated, associations, likely, corrected, consistent, reported, result, implicated, explained, explained by, show, shown, accordance, evidence, evidence-based replicated, objective, consistency, effects, extends, positive, meaningful, follow, for example, proof, increasing proof, incorporated, assessed, verified, utilizing, augment, relationship linked, connections, probable, adjusted, aligned, documented, outcome, suggested, justified, attributed to, demonstrate, demonstrated, alignment, findings, fact-based reproduced, factual, uniformity, impacts, broadens, beneficial, significant, adhere, such as'" />
    <xsl:variable name="negative-words" select="'lack, few, few examples, inconsistent, bias, insufficient, risk, inconsistency, imprecise, subjectively, subjective, however unclear, mixed, mixed findings, inconclusive, scarcity, limitation, sparsity, variability, partiality, inadequacy, insufficiency, uncertainty, variability, approximation, interpretation, opinionatedness, individual perspective, even though, vagueness, contradiction, divergent conclusions, unresolved evidence, equivocal results, lack of clarity, inconsistency, conflicting interpretations, tentative evidence, provisional outcomes, unreliability'" />
    
    <!-- transformation to copy -->
    <xsl:template match="node()|@*">
        <xsl:copy>
            <xsl:apply-templates select="node()|@*" />
        </xsl:copy>
    </xsl:template>
    
    <!-- match paragraph elements -->
    <xsl:template match="p">
        <xsl:copy>
            <xsl:apply-templates select="@*" />
            <!-- Iterate over child nodes and text -->
            <xsl:for-each select="node()|text()">
                <xsl:variable name="current-content">
                    <xsl:apply-templates select="." mode="as-string" />
                </xsl:variable>
                <xsl:variable name="is-positive">
                    <xsl:call-template name="contains-any">
                        <xsl:with-param name="text" select="$current-content" />
                        <xsl:with-param name="word-list" select="$positive-words" />
                    </xsl:call-template>
                </xsl:variable>
                <xsl:variable name="is-negative">
                    <xsl:call-template name="contains-any">
                        <xsl:with-param name="text" select="$current-content" />
                        <xsl:with-param name="word-list" select="$negative-words" />
                    </xsl:call-template>
                </xsl:variable>
                <xsl:choose>
                    <!--  positive content -->
                    <xsl:when test="$is-positive = 'true'">
                        <citation_analysis attribute="positive">
                            <xsl:apply-templates select="." />
                        </citation_analysis>
                    </xsl:when>
                    <!--negative content -->
                    <xsl:when test="$is-negative = 'true'">
                        <citation_analysis attribute="negative">
                            <xsl:apply-templates select="." />
                        </citation_analysis>
                    </xsl:when>
                    <!-- neutral content -->
                    <xsl:otherwise>
                        <citation_analysis attribute="neither">
                            <xsl:apply-templates select="." />
                        </citation_analysis>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:for-each>
        </xsl:copy>
    </xsl:template>
    
    <!-- concatenate text and inline elements into a single string -->
    <xsl:template match="node()|text()" mode="as-string">
        <xsl:choose>
            <xsl:when test="self::text()">
                <xsl:value-of select="normalize-space(.)" />
            </xsl:when>
            <xsl:when test="self::xref">
                <xsl:value-of select="concat(' ', .)" />
            </xsl:when>
        </xsl:choose>
    </xsl:template>
    
    <!-- check if a string contains any word from a list -->
    <xsl:template name="contains-any">
        <xsl:param name="text" />
        <xsl:param name="word-list" />
        <xsl:variable name="first-word" select="substring-before($word-list, ',')" />
        <xsl:choose>
            <!-- match found -->
            <xsl:when test="contains(concat(' ', $text, ' '), concat(' ', normalize-space($first-word), ' '))">
                <xsl:value-of select="'true'" />
            </xsl:when>
            <!-- check remaining words -->
            <xsl:when test="contains($word-list, ',')">
                <xsl:call-template name="contains-any">
                    <xsl:with-param name="text" select="$text" />
                    <xsl:with-param name="word-list" select="substring-after($word-list, ',')" />
                </xsl:call-template>
            </xsl:when>
            <!-- no match found -->
            <xsl:otherwise>
                <xsl:value-of select="'false'" />
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
</xsl:stylesheet>