===========================
Illustrate Mermaid Diagrams
===========================

:Authors:
    Cao Tri DO <cao-tri.do@keyrus.com>
:Version: 2025-02

Flowcharts graph
=================
The graph below gives an overview of the interactions between some **Services** in an **ecosystem**:

.. tab:: The beautiful Flowchart

  .. mermaid::

    flowchart LR
        subgraph Datacenter Region X
          webapp(Web Application)-- REST ---api(API)--- api_db[(API Database)]
          api---redis[(Redis Database)]---consumer(Consumer)
        end
        subgraph Main Datacenter
          hub(Hub)---hub_db[(Hub Database)]
          hub---hub_fs[(Document Storage)]
        end
        subgraph Keyrus
          thegate(Gate)-- SSO ---webapp
          thegate-- Token Verification ---api
          dms(DMS)-- HTTP ---api
          dms-- HTTP ---hub
          mailer(Mailer)---api
        end
        webapp-- REST ---hub
        api-- REST readonly ---hub

.. tab:: show me the 17 lines of low code to create it

  .. code::

    .. mermaid::

      flowchart LR
          subgraph Datacenter Region X
            webapp(Web Application)-- REST ---api(API)--- api_db[(API Database)]
            api---redis[(Redis Database)]---consumer(Consumer)
          end
          subgraph Main Datacenter
            hub(Hub)---hub_db[(Hub Database)]
            hub---hub_fs[(Document Storage)]
          end
          subgraph Keyrus
            thegate(Gate)-- SSO ---webapp
            thegate-- Token Verification ---api
            dms(DMS)-- HTTP ---api
            dms-- HTTP ---hub
            mailer(Mailer)---api
          end

          webapp-- REST ---hub
          api-- REST readonly ---hub

ER Diagram
==========

.. tab:: ER Diagram

  .. mermaid::

    erDiagram

        DIM_CUSTOMER {
            string name
            string custNumber
            string sector
        }

        FACT_ORDER {
            int orderNumber
            string productCode
            string custNumber
            string deliveryAddress
        }
        DIM_ITEM {
            string productCode
            int quantity
            float pricePerUnit
        }

        FACT_ORDER ||--|{ DIM_CUSTOMER : contains
        FACT_ORDER ||--|{ DIM_ITEM : contains

.. tab:: ER diagram in a few lines of codes

  .. code::

    .. mermaid::

      erDiagram

          DIM_CUSTOMER {
              string name
              string custNumber
              string sector
          }

          FACT_ORDER {
              int orderNumber
              string productCode
              string custNumber
              string deliveryAddress
          }
          DIM_ITEM {
              string productCode
              int quantity
              float pricePerUnit
          }

          FACT_ORDER ||--|{ DIM_CUSTOMER : contains
          FACT_ORDER ||--|{ DIM_ITEM : contains

Measure Depedency diagram
=========================

This can be interested when you want to extract the dependency between your measure in a Power BI Report

.. tab:: Depedency diagram

  .. mermaid::

    flowchart LR
    %% Measure dependancy mermaid flowchart

    %% [Revenue Won] Dependancies:
      4175e2ae-8428-461a-854b-9a68cf5b5b8c["Revenue Won"]

    %% [Revenue In Pipeline] Dependancies:
      1322f812-7712-498e-9f4d-ba6b80052388["Revenue In Pipeline"]
      30a1a858-afcc-4343-802b-5b2229eccc0e["Forecast Adjustment Value"] --> 1322f812-7712-498e-9f4d-ba6b80052388["Revenue In Pipeline"]

    %% [Forecast %] Dependancies:
      78a5c219-6674-49f8-a2c5-4da21114763d["Forecast %"]
      4175e2ae-8428-461a-854b-9a68cf5b5b8c["Revenue Won"] --> 78a5c219-6674-49f8-a2c5-4da21114763d["Forecast %"]
      1322f812-7712-498e-9f4d-ba6b80052388["Revenue In Pipeline"] --> 78a5c219-6674-49f8-a2c5-4da21114763d["Forecast %"]
      3cd274e0-076f-46e7-b6f2-3d9f5312d8f2["Rev Goal"] --> 78a5c219-6674-49f8-a2c5-4da21114763d["Forecast %"]

    %% [Forecast] Dependancies:
      f3eb5c0a-9667-445a-b762-e4e9f911c533["Forecast"]
      4175e2ae-8428-461a-854b-9a68cf5b5b8c["Revenue Won"] --> f3eb5c0a-9667-445a-b762-e4e9f911c533["Forecast"]
      1322f812-7712-498e-9f4d-ba6b80052388["Revenue In Pipeline"] --> f3eb5c0a-9667-445a-b762-e4e9f911c533["Forecast"]

    %% [Opportunity Count In Pipeline] Dependancies:
      b4effa85-1aa3-4f33-a3ef-07ec57b59c0f["Opportunity Count In Pipeline"]

    %% [Opportunity Count] Dependancies:
      f9cdd5b7-71b0-42ca-b100-d957cbdaa375["Opportunity Count"]

    %% [Count of Won] Dependancies:
      61908284-58b6-4ce1-b980-2cd65b89fafd["Count of Won"]

    %% [Count of Lost] Dependancies:
      0995fcc4-bb40-4d35-aac9-9ecf60f69bbe["Count of Lost"]

    %% [Close %] Dependancies:
      938be727-4972-4ef9-a507-da6a1d898703["Close %"]
      61908284-58b6-4ce1-b980-2cd65b89fafd["Count of Won"] --> 938be727-4972-4ef9-a507-da6a1d898703["Close %"]
      0995fcc4-bb40-4d35-aac9-9ecf60f69bbe["Count of Lost"] --> 938be727-4972-4ef9-a507-da6a1d898703["Close %"]

    %% [Revenue Open] Dependancies:
      d8ffa47c-94b4-4585-9170-43b31ec2dd1d["Revenue Open"]
      30a1a858-afcc-4343-802b-5b2229eccc0e["Forecast Adjustment Value"] --> d8ffa47c-94b4-4585-9170-43b31ec2dd1d["Revenue Open"]

    %% [Revenue Won Average Deal Size] Dependancies:
      959e44c7-e496-4ebb-8687-668c3c16f605["Revenue Won Average Deal Size"]
      4175e2ae-8428-461a-854b-9a68cf5b5b8c["Revenue Won"] --> 959e44c7-e496-4ebb-8687-668c3c16f605["Revenue Won Average Deal Size"]

    %% [Forecast by Win/Loss Ratio] Dependancies:
      25b97fa8-199c-498f-9c14-f5e7d8cbb022["Forecast by Win/Loss Ratio"]
      d8ffa47c-94b4-4585-9170-43b31ec2dd1d["Revenue Open"] --> 25b97fa8-199c-498f-9c14-f5e7d8cbb022["Forecast by Win/Loss Ratio"]
      938be727-4972-4ef9-a507-da6a1d898703["Close %"] --> 25b97fa8-199c-498f-9c14-f5e7d8cbb022["Forecast by Win/Loss Ratio"]

    %% [Close target] Dependancies:
      bb1a15f8-95da-4d20-b5d7-c4d19a8187f5["Close target"]

    %% [AVG Days to Close] Dependancies:
      fc83e054-2114-4326-ae63-f0b2a1f0daff["AVG Days to Close"]

    %% [Rev Goal] Dependancies:
      3cd274e0-076f-46e7-b6f2-3d9f5312d8f2["Rev Goal"]
      4175e2ae-8428-461a-854b-9a68cf5b5b8c["Revenue Won"] --> 3cd274e0-076f-46e7-b6f2-3d9f5312d8f2["Rev Goal"]

    %% [Revenue Won - MoM %] Dependancies:
      5d814897-7599-40a1-9dfc-4a61042c2c3a["Revenue Won - MoM %"]
      4175e2ae-8428-461a-854b-9a68cf5b5b8c["Revenue Won"] --> 5d814897-7599-40a1-9dfc-4a61042c2c3a["Revenue Won - MoM %"]

    %% [Opportunities Created - MoM % Change] Dependancies:
      d5538591-9b31-4520-8434-12b904816180["Opportunities Created - MoM % Change"]
      234108f0-185a-4870-ad95-73cc7499113a["Opportunities Created"] --> d5538591-9b31-4520-8434-12b904816180["Opportunities Created - MoM % Change"]

    %% [Opportunities Created] Dependancies:
      234108f0-185a-4870-ad95-73cc7499113a["Opportunities Created"]

    %% [Count of Open] Dependancies:
      2218a695-b4e6-427a-a9cd-00bdda86b3da["Count of Open"]

    %% [Forecast Adjustment Value] Dependancies:
      30a1a858-afcc-4343-802b-5b2229eccc0e["Forecast Adjustment Value"]

.. tab:: Depedency diagram in a few lines

  .. code::

    .. mermaid::

      flowchart LR
      %% Measure dependancy mermaid flowchart

      %% [Revenue Won] Dependancies:
        4175e2ae-8428-461a-854b-9a68cf5b5b8c["Revenue Won"]

      %% [Revenue In Pipeline] Dependancies:
        1322f812-7712-498e-9f4d-ba6b80052388["Revenue In Pipeline"]
        30a1a858-afcc-4343-802b-5b2229eccc0e["Forecast Adjustment Value"] --> 1322f812-7712-498e-9f4d-ba6b80052388["Revenue In Pipeline"]

      %% [Forecast %] Dependancies:
        78a5c219-6674-49f8-a2c5-4da21114763d["Forecast %"]
        4175e2ae-8428-461a-854b-9a68cf5b5b8c["Revenue Won"] --> 78a5c219-6674-49f8-a2c5-4da21114763d["Forecast %"]
        1322f812-7712-498e-9f4d-ba6b80052388["Revenue In Pipeline"] --> 78a5c219-6674-49f8-a2c5-4da21114763d["Forecast %"]
        3cd274e0-076f-46e7-b6f2-3d9f5312d8f2["Rev Goal"] --> 78a5c219-6674-49f8-a2c5-4da21114763d["Forecast %"]

      %% [Forecast] Dependancies:
        f3eb5c0a-9667-445a-b762-e4e9f911c533["Forecast"]
        4175e2ae-8428-461a-854b-9a68cf5b5b8c["Revenue Won"] --> f3eb5c0a-9667-445a-b762-e4e9f911c533["Forecast"]
        1322f812-7712-498e-9f4d-ba6b80052388["Revenue In Pipeline"] --> f3eb5c0a-9667-445a-b762-e4e9f911c533["Forecast"]

      %% [Opportunity Count In Pipeline] Dependancies:
        b4effa85-1aa3-4f33-a3ef-07ec57b59c0f["Opportunity Count In Pipeline"]

      %% [Opportunity Count] Dependancies:
        f9cdd5b7-71b0-42ca-b100-d957cbdaa375["Opportunity Count"]

      %% [Count of Won] Dependancies:
        61908284-58b6-4ce1-b980-2cd65b89fafd["Count of Won"]

      %% [Count of Lost] Dependancies:
        0995fcc4-bb40-4d35-aac9-9ecf60f69bbe["Count of Lost"]

      %% [Close %] Dependancies:
        938be727-4972-4ef9-a507-da6a1d898703["Close %"]
        61908284-58b6-4ce1-b980-2cd65b89fafd["Count of Won"] --> 938be727-4972-4ef9-a507-da6a1d898703["Close %"]
        0995fcc4-bb40-4d35-aac9-9ecf60f69bbe["Count of Lost"] --> 938be727-4972-4ef9-a507-da6a1d898703["Close %"]

      %% [Revenue Open] Dependancies:
        d8ffa47c-94b4-4585-9170-43b31ec2dd1d["Revenue Open"]
        30a1a858-afcc-4343-802b-5b2229eccc0e["Forecast Adjustment Value"] --> d8ffa47c-94b4-4585-9170-43b31ec2dd1d["Revenue Open"]

      %% [Revenue Won Average Deal Size] Dependancies:
        959e44c7-e496-4ebb-8687-668c3c16f605["Revenue Won Average Deal Size"]
        4175e2ae-8428-461a-854b-9a68cf5b5b8c["Revenue Won"] --> 959e44c7-e496-4ebb-8687-668c3c16f605["Revenue Won Average Deal Size"]

      %% [Forecast by Win/Loss Ratio] Dependancies:
        25b97fa8-199c-498f-9c14-f5e7d8cbb022["Forecast by Win/Loss Ratio"]
        d8ffa47c-94b4-4585-9170-43b31ec2dd1d["Revenue Open"] --> 25b97fa8-199c-498f-9c14-f5e7d8cbb022["Forecast by Win/Loss Ratio"]
        938be727-4972-4ef9-a507-da6a1d898703["Close %"] --> 25b97fa8-199c-498f-9c14-f5e7d8cbb022["Forecast by Win/Loss Ratio"]

      %% [Close target] Dependancies:
        bb1a15f8-95da-4d20-b5d7-c4d19a8187f5["Close target"]

      %% [AVG Days to Close] Dependancies:
        fc83e054-2114-4326-ae63-f0b2a1f0daff["AVG Days to Close"]

      %% [Rev Goal] Dependancies:
        3cd274e0-076f-46e7-b6f2-3d9f5312d8f2["Rev Goal"]
        4175e2ae-8428-461a-854b-9a68cf5b5b8c["Revenue Won"] --> 3cd274e0-076f-46e7-b6f2-3d9f5312d8f2["Rev Goal"]

      %% [Revenue Won - MoM %] Dependancies:
        5d814897-7599-40a1-9dfc-4a61042c2c3a["Revenue Won - MoM %"]
        4175e2ae-8428-461a-854b-9a68cf5b5b8c["Revenue Won"] --> 5d814897-7599-40a1-9dfc-4a61042c2c3a["Revenue Won - MoM %"]

      %% [Opportunities Created - MoM % Change] Dependancies:
        d5538591-9b31-4520-8434-12b904816180["Opportunities Created - MoM % Change"]
        234108f0-185a-4870-ad95-73cc7499113a["Opportunities Created"] --> d5538591-9b31-4520-8434-12b904816180["Opportunities Created - MoM % Change"]

      %% [Opportunities Created] Dependancies:
        234108f0-185a-4870-ad95-73cc7499113a["Opportunities Created"]

      %% [Count of Open] Dependancies:
        2218a695-b4e6-427a-a9cd-00bdda86b3da["Count of Open"]

      %% [Forecast Adjustment Value] Dependancies:
        30a1a858-afcc-4343-802b-5b2229eccc0e["Forecast Adjustment Value"]




sequenceDiagram
==================
Serious software should consume his own API REST or GraphQL, this API should
has to be correctly documented in term of **sequenceDiagram** including the
Token security layer.

.. tab:: sequenceDiagram

  .. mermaid::

    sequenceDiagram

      App1 ->>+ Gate: Request Access token
      Gate -->>- App1: Access Token
      App1 ->>+ API Gateway: api/engagements/webhook + Access Token
      API Gateway ->>+ Gate: Validate token
      Gate -->>- API Gateway: Token information
      alt Token is valid
          API Gateway->> API Gateway: Identify consumer
      else Token is invalid or consumer is unknown
          API Gateway-->> App1: Not Authorized
      end
      API Gateway->>+ App2: Forward api/engagements/webhook + Access Token
      App2 ->>+ Gate: Validate token
      Gate -->>- App2: Token information
      alt Token is valid
          App2 ->> App2: Authorize consumer
          App2 -->> API Gateway: Response payload (ACK/NACK)
          API Gateway-->> App1: Forward Response payload (ACK/NACK)
          App2 ->> App1: Execute request
      else Token is invalid or consumer is unknown
          App2 -->>- API Gateway: Not Authorized
          API Gateway-->>- App2: Not Authorized
      end

.. tab:: sequenceDiagram only 23 lines of low code ;)

  .. code::

    .. mermaid::

      sequenceDiagram

        App2 ->>+ Gate: Request Access token
        Gate -->>- App2: Access Token
        AtlasBlue ->>+ API Gateway: api/engagements/webhook + Access Token
        API Gateway ->>+ Gate: Validate token
        Gate -->>- API Gateway: Token information
        alt Token is valid
            API Gateway->> API Gateway: Identify consumer
        else Token is invalid or consumer is unknown
            API Gateway-->> App2: Not Authorized
        end
        API Gateway->>+ App2: Forward api/engagements/webhook + Access Token
        App2 ->>+ Gate: Validate token
        Gate -->>- App2: Token information
        alt Token is valid
            App2 ->> App2: Authorize consumer
            App2 -->> API Gateway: Response payload (ACK/NACK)
            API Gateway-->> App2: Forward Response payload (ACK/NACK)
            App2 ->> App2: Execute request
        else Token is invalid or consumer is unknown
            App2 -->>- API Gateway: Not Authorized
            API Gateway-->>- App2: Not Authorized
        end

Gantt Diagram
================
.. tab:: To have the project done on time

  .. mermaid::

    gantt
      title My Super Assistant Planning
      dateFormat  YY-MM-DD
      axisFormat  %Y-%m

      section main
        Input / Mapping (From RA)      :active, map1,  21-12-10,    1w
        Input / Mapping (from AnaBlue) :active, map2, after ex_1,   5w
        Input / Mapping (from AnaBlue) :active, map3, after spring, 2w

      section Holidays
        Christmas                 :done,   chris,  21-12-22, 22-01-02
        spring                    :done,   spring, 22-03-21, 22-04-05

      section Core Model
        Core FSA                  :active, core,  after clas,   3w
        T1 Simples                :active, t1,    after core,   4w
        T2 External Files + samp  :active, t2, after fsa_1, 3w
        T3 JE + duplicate         :active, t3, after fsa_4   , 5w

      section FSA Tresorerie
        FSA.tests all             :active, fsa_1, after chris,    2w
        Workpaper Excel           :active, ex_1,  after fsa_1, 4w

      section FSA AACE
        FSA.tests T1 T2      :active, fsa_3, after fsa_2,    2w
        Workpaper Excel      :active, ex_3,  after fsa_3, 2w

      section Fournisseurs
        FSA.tests T1 T2      :active, fsa_4, after fsa_3, 2w
        Workpaper Excel      :active, ex_4,  after fsa_4, 2w

.. tab:: Gantt only 25 lines of low code ;)

  .. code::

    .. mermaid::

      gantt
        title My Super Assistant Planning
        dateFormat  YY-MM-DD
        axisFormat  %Y-%m

        section main
          Input / Mapping (From RA)      :active, map1,  21-12-10,    1w
          Input / Mapping (from AnaBlue) :active, map2, after ex_1,   5w
          Input / Mapping (from AnaBlue) :active, map3, after spring, 2w

        section Holidays
          Christmas                 :done,   chris,  21-12-22, 22-01-02
          spring                    :done,   spring, 22-03-21, 22-04-05

        section Core Model
          Core FSA                  :active, core,  after clas,   3w
          T1 Simples                :active, t1,    after core,   4w
          T2 External Files + samp  :active, t2, after fsa_1, 3w
          T3 JE + duplicate         :active, t3, after fsa_4   , 5w

        section FSA Tresorerie
          FSA.tests all             :active, fsa_1, after chris,    2w
          Workpaper Excel           :active, ex_1,  after fsa_1, 4w

        section FSA AACE
          FSA.tests T1 T2      :active, fsa_3, after fsa_2,    2w
          Workpaper Excel      :active, ex_3,  after fsa_3, 2w

        section Fournisseurs
          FSA.tests T1 T2      :active, fsa_4, after fsa_3, 2w
          Workpaper Excel      :active, ex_4,  after fsa_4, 2w


Bibliography
=============

- https://mermaid-js.github.io/mermaid/#/flowchart
- https://github.com/mermaid-js/mermaid-cli
