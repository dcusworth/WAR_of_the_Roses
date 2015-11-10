## Title of Project
The WAR of Roses. How to predict "True Love" from 20 Seasons of ABC's \textit{The Bachelor}.

## Team Name
Team Bootleg Fireworks

## Background and Motivation
Reality television has become a staple of modern popular culture. The popular television show The Bachelor garners on average 7 million viewers a week. Even under the guise of "reality" and "true love," we hypothesize that there exist underlying patterns that in general enhance a contestant's chance of winning. As a "game," we propose to create a dynamic model that is updated each week of the competition, and can used to predict a contestant's chance of winning the competition.

## Project Objectives
The objective of this project is to create a dynamic model that can be used to predict the winner of The Bachelor. We want to understand how much a person's physical appearance, background information, and performance on each episode of the show contribute to their overall performance. We wish to learn more about unsupervised classification and prediction methods.

## What Data
For each season (19 total), we can obtain each person's name, age (at the start of the competition), and profession online from Wikipedia as well as other sources. Wikipedia also contains each's contestant's performance for a certain week (e.g. received a rose, was eliminated, received a date). We will need to scrape other websites for studio photographs of each contestants. We will use this to perform PCA on each contestant's photo.

## Must Have Features
We must at least have a statistical model that predict's each contestant's probability to win the whole competition based on their background information (initialization), and their subsequent performance on each week's episode. The probabilities will update each week as some contestants are eliminated and others better capture the attention of the Bachelor.

## Optional Features
We would like to find transcripts of each episode to quantify how much each contestant is featured in each episode, and see how it relates to their overall performance. 

## Design Overview
Step 1: Run PCA on each contestant's photo and combine it with background information (age, profession, hometown) to create a baseline prediction of winner the television show.
Step 2: Each week of the show, update the probabilities of winning the competition depending on a contestant's performance (got a date, got a rose, potentially screen time via transcripts) using linear regression.
For each Step 1 and 2, we will devise a weighting scheme which takes into account each feature type as well as time (e.g. results from week 1 of the competition receive less weight than results from week 4).

## Verification
We plan to combine all 19 seasons of data and then perform leave-one-out cross validation. Our test set will be the 20th season of the Bachelor starting winter of 2016.

## Visualization & Presentation
We plan to show clips from the television show to introduce the format of the game, and what features we find important to the analyis. We will provide voice-overs to highlight key points to the audience. For the website, we plan to guide the reader through a week-by-week synopsis, showing how probabilities change as the show unfolds.

## Schedule / timeline
 
